#!/usr/bin/env python
# crate_anon/crateweb/consent/models.py

"""
===============================================================================
    Copyright (C) 2015-2017 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of CRATE.

    CRATE is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    CRATE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CRATE. If not, see <http://www.gnu.org/licenses/>.
===============================================================================
"""

import datetime
from dateutil.relativedelta import relativedelta
import logging
from operator import attrgetter
import os
import re
from typing import Any, List, Optional, Tuple, Type, Union

# from audit_log.models import AuthStampedModel  # django-audit-log
from django import forms
from django.conf import settings
from django.core.exceptions import (
    MultipleObjectsReturned,
    ObjectDoesNotExist,
    ValidationError,
)
from django.core.mail import EmailMessage, EmailMultiAlternatives
# from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.db import connections, models, transaction
from django.db.models import Q, QuerySet
from django.dispatch import receiver
from django.http import QueryDict, Http404
from django.http.request import HttpRequest
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.functional import cached_property

from crate_anon.common.lang import simple_repr
from crate_anon.common.contenttypes import CONTENTTYPE_PDF
from crate_anon.crateweb.core.constants import (
    LEN_ADDRESS,
    LEN_FIELD_DESCRIPTION,
    LEN_NAME,
    LEN_PHONE,
    LEN_TITLE,
    MAX_HASH_LENGTH,
)
from crate_anon.crateweb.core.dbfunc import (
    dictfetchall,
    dictfetchone,
    fetchallfirstvalues,
)
from crate_anon.crateweb.core.utils import (
    modelrepr,
    site_absolute_url,
    string_time_now,
    url_with_querystring,
)
from crate_anon.crateweb.extra.admin import admin_view_url
from crate_anon.crateweb.extra.fields import (
    auto_delete_files_on_instance_change,
    auto_delete_files_on_instance_delete,
    choice_explanation,
    ContentTypeRestrictedFileField,
    # IsoDateTimeTzField,
)
from crate_anon.crateweb.extra.pdf import (
    get_concatenated_pdf_in_memory,
    pdf_from_html,
    PdfPlan,
)
from crate_anon.crateweb.extra.salutation import (
    forename_surname,
    get_initial_surname_tuple_from_string,
    salutation,
    title_forename_surname,
)
from crate_anon.crateweb.research.models import get_mpid
from crate_anon.crateweb.consent.storage import privatestorage
from crate_anon.crateweb.consent.tasks import (
    email_rdbm_task,
    process_contact_request,
)
from crate_anon.crateweb.consent.utils import (
    days_to_years,
    latest_date,
    render_email_html_to_string,
    render_pdf_html_to_string,
    validate_researcher_email_domain,
)
from crate_anon.preprocess.rio_constants import (
    CRATE_COL_RIO_NUMBER,
    RCEP_COL_PATIENT_ID,
)

log = logging.getLogger(__name__)

CLINICIAN_RESPONSE_FWD_REF = "ClinicianResponse"
CONSENT_MODE_FWD_REF = "ConsentMode"
CONTACT_REQUEST_FWD_REF = "ContactRequest"
EMAIL_FWD_REF = "Email"
EMAIL_TRANSMISSION_FWD_REF = "EmailTransmission"
LEAFLET_FWD_REF = "Leaflet"
LETTER_FWD_REF = "Letter"
STUDY_FWD_REF = "Study"

SOURCE_DB_NAME_MAX_LENGTH = 20

TEST_ID = -1
TEST_ID_STR = str(TEST_ID)


# =============================================================================
# Study
# =============================================================================

def study_details_upload_to(instance: STUDY_FWD_REF, filename: str) -> str:
    """
    Determines the filename used for study information PDF uploads.
    instance = instance of Study (potentially unsaved)
        ... and you can't call save(); it goes into infinite recursion
    filename = uploaded filename
    """
    extension = os.path.splitext(filename)[1]  # includes the '.' if present
    return os.path.join("study", "{}_details_{}{}".format(
        instance.institutional_id,
        string_time_now(),
        extension))
    # ... as id may not exist yet


def study_form_upload_to(instance: STUDY_FWD_REF, filename: str) -> str:
    """
    Determines the filename used for study clinician-form PDF uploads.
    instance = instance of Study (potentially unsaved)
    filename = uploaded filename
    """
    extension = os.path.splitext(filename)[1]
    return os.path.join("study", "{}_form_{}{}".format(
        instance.institutional_id,
        string_time_now(),
        extension))


class Study(models.Model):
    # implicit 'id' field
    institutional_id = models.PositiveIntegerField(
        verbose_name="Institutional (e.g. NHS Trust) study number",
        unique=True)
    title = models.CharField(max_length=255, verbose_name="Study title")
    lead_researcher = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        related_name="studies_as_lead")
    researchers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name="studies_as_researcher",
                                         blank=True)
    registered_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name="When was the study registered?")
    summary = models.TextField(verbose_name="Summary of study")
    search_methods_planned = models.TextField(
        blank=True,
        verbose_name="Search methods planned")
    patient_contact = models.BooleanField(
        verbose_name="Involves patient contact?")
    include_under_16s = models.BooleanField(
        verbose_name="Include patients under 16?")
    include_lack_capacity = models.BooleanField(
        verbose_name="Include patients lacking capacity?")
    clinical_trial = models.BooleanField(
        verbose_name="Clinical trial (CTIMP)?")
    include_discharged = models.BooleanField(
        verbose_name="Include discharged patients?")
    request_direct_approach = models.BooleanField(
        verbose_name="Researchers request direct approach to patients?")
    approved_by_rec = models.BooleanField(
        verbose_name="Approved by REC?")
    rec_reference = models.CharField(
        max_length=50, blank=True,
        verbose_name="Research Ethics Committee reference")
    approved_locally = models.BooleanField(
        verbose_name="Approved by local institution?")
    local_approval_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name="When approved by local institution?")
    study_details_pdf = ContentTypeRestrictedFileField(
        blank=True,
        storage=privatestorage,
        content_types=[CONTENTTYPE_PDF],
        max_upload_size=settings.MAX_UPLOAD_SIZE_BYTES,
        upload_to=study_details_upload_to)
    subject_form_template_pdf = ContentTypeRestrictedFileField(
        blank=True,
        storage=privatestorage,
        content_types=[CONTENTTYPE_PDF],
        max_upload_size=settings.MAX_UPLOAD_SIZE_BYTES,
        upload_to=study_form_upload_to)
    # http://nemesisdesign.net/blog/coding/django-private-file-upload-and-serving/  # noqa
    # http://stackoverflow.com/questions/8609192/differentiate-null-true-blank-true-in-django  # noqa
    AUTODELETE_OLD_FILE_FIELDS = ['study_details_pdf',
                                  'subject_form_template_pdf']

    class Meta:
        verbose_name_plural = "studies"

    def __str__(self):
        return "[Study {}] {}: {} / {}".format(
            self.id,
            self.institutional_id,
            self.lead_researcher.get_full_name(),
            self.title
        )

    def get_lead_researcher_name_address(self) -> List[str]:
        return (
            [self.lead_researcher.profile.get_title_forename_surname()] +
            self.lead_researcher.profile.get_address_components()
        )

    def get_lead_researcher_salutation(self) -> str:
        return self.lead_researcher.profile.get_salutation()

    def get_involves_lack_of_capacity(self) -> str:
        if not self.include_lack_capacity:
            return "No"
        if self.clinical_trial:
            return "Yes (and it is a clinical trial)"
        return "Yes (and it is not a clinical trial)"

    @staticmethod
    def filter_studies_for_researcher(
            queryset: QuerySet,
            user: settings.AUTH_USER_MODEL) -> QuerySet:
        return queryset.filter(Q(lead_researcher=user) |
                               Q(researchers__in=[user]))\
                       .distinct()


# noinspection PyUnusedLocal
@receiver(models.signals.post_delete, sender=Study)
def auto_delete_study_files_on_delete(sender: Type[Study],
                                      instance: Study,
                                      **kwargs: Any) -> None:
    """Deletes files from filesystem when Study object is deleted."""
    auto_delete_files_on_instance_delete(instance,
                                         Study.AUTODELETE_OLD_FILE_FIELDS)


# noinspection PyUnusedLocal
@receiver(models.signals.pre_save, sender=Study)
def auto_delete_study_files_on_change(sender: Type[Study],
                                      instance: Study,
                                      **kwargs: Any) -> None:
    """Deletes files from filesystem when Study object is changed."""
    auto_delete_files_on_instance_change(instance,
                                         Study.AUTODELETE_OLD_FILE_FIELDS,
                                         Study)


# =============================================================================
# Generic leaflets
# =============================================================================

def leaflet_upload_to(instance: LEAFLET_FWD_REF, filename: str) -> str:
    """
    Determines the filename used for leaflet uploads.
    instance = instance of Leaflet (potentially unsaved)
        ... and you can't call save(); it goes into infinite recursion
    filename = uploaded filename
    """
    extension = os.path.splitext(filename)[1]  # includes the '.' if present
    return os.path.join("leaflet", "{}_{}{}".format(
        instance.name,
        string_time_now(),
        extension))
    # ... as id may not exist yet


class Leaflet(models.Model):
    CPFT_TPIR = 'cpft_tpir'  # mandatory
    NIHR_YHRSL = 'nihr_yhrsl'  # not used automatically
    CPFT_TRAFFICLIGHT_CHOICE = 'cpft_trafficlight_choice'
    CPFT_CLINRES = 'cpft_clinres'

    LEAFLET_CHOICES = (
        (CPFT_TPIR, 'CPFT: Taking part in research [MANDATORY]'),
        (NIHR_YHRSL,
         'NIHR: Your health records save lives [not currently used]'),
        (CPFT_TRAFFICLIGHT_CHOICE,
         'CPFT: traffic-light choice decision form [not currently used: '
         'personalized version created instead]'),
        (CPFT_CLINRES, 'CPFT: clinical research [not currently used]'),
    )
    # https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.Field.choices  # noqa

    name = models.CharField(max_length=50, unique=True,
                            choices=LEAFLET_CHOICES,
                            verbose_name="leaflet name")
    pdf = ContentTypeRestrictedFileField(
        blank=True,
        storage=privatestorage,
        content_types=[CONTENTTYPE_PDF],
        max_upload_size=settings.MAX_UPLOAD_SIZE_BYTES,
        upload_to=leaflet_upload_to)

    def __str__(self):
        for x in Leaflet.LEAFLET_CHOICES:
            if x[0] == self.name:
                name = x[1]
                if not self.pdf:
                    name += " (MISSING)"
                return name
        return "? (bad name: {})".format(self.name)

    @staticmethod
    def populate() -> None:
        # Pre-create instances
        keys = [x[0] for x in Leaflet.LEAFLET_CHOICES]
        for x in keys:
            if not Leaflet.objects.filter(name=x).exists():
                obj = Leaflet(name=x)
                obj.save()


# noinspection PyUnusedLocal
@receiver(models.signals.post_delete, sender=Leaflet)
def auto_delete_leaflet_files_on_delete(sender: Type[Leaflet],
                                        instance: Leaflet,
                                        **kwargs: Any) -> None:
    """Deletes files from filesystem when Leaflet object is deleted."""
    auto_delete_files_on_instance_delete(instance, ['pdf'])


# noinspection PyUnusedLocal
@receiver(models.signals.pre_save, sender=Leaflet)
def auto_delete_leaflet_files_on_change(sender: Type[Leaflet],
                                        instance: Leaflet,
                                        **kwargs: Any) -> None:
    """Deletes files from filesystem when Leaflet object is changed."""
    auto_delete_files_on_instance_change(instance, ['pdf'], Leaflet)


# =============================================================================
# Generic fields for decisions
# =============================================================================

class Decision(models.Model):
    # Note that Decision._meta.get_fields() doesn't care about the
    # ordering of its fields (and, I think, they can change). So:
    FIELDS = [
        'decision_signed_by_patient',
        'decision_otherwise_directly_authorized_by_patient',
        'decision_under16_signed_by_parent',
        'decision_under16_signed_by_clinician',
        'decision_lack_capacity_signed_by_representative',
        'decision_lack_capacity_signed_by_clinician',
    ]
    decision_signed_by_patient = models.BooleanField(
        default=False,
        verbose_name="Request signed by patient?")
    decision_otherwise_directly_authorized_by_patient = models.BooleanField(
        default=False,
        verbose_name="Request otherwise directly authorized by patient?")
    decision_under16_signed_by_parent = models.BooleanField(
        default=False,
        verbose_name="Patient under 16 and request countersigned by parent?")
    decision_under16_signed_by_clinician = models.BooleanField(
        default=False,
        verbose_name="Patient under 16 and request countersigned by "
                     "clinician?")
    decision_lack_capacity_signed_by_representative = models.BooleanField(
        default=False,
        verbose_name="Patient lacked capacity and request signed by "
                     "authorized representative?")
    decision_lack_capacity_signed_by_clinician = models.BooleanField(
        default=False,
        verbose_name="Patient lacked capacity and request countersigned by "
                     "clinician?")

    class Meta:
        abstract = True

    def decision_valid(self) -> bool:
        # We can never electronically validate being under 16 (time may have
        # passed since the lookup) or, especially, lacking capacity, so let's
        # just trust the user
        return (
            self.decision_signed_by_patient or
            self.decision_otherwise_directly_authorized_by_patient
        ) or (
            # Lacks capacity
            self.decision_lack_capacity_signed_by_representative and
            self.decision_lack_capacity_signed_by_clinician
        ) or (
            # Under 16: 2/3 rule
            int(self.decision_signed_by_patient or
                self.decision_otherwise_directly_authorized_by_patient) +
            int(self.decision_under16_signed_by_parent) +
            int(self.decision_under16_signed_by_clinician) >= 2
            # I know the logic overlaps. But there you go.
        )

    def validate_decision(self) -> None:
        if not self.decision_valid():
            raise forms.ValidationError(
                "Invalid decision. Options are: "
                "(*) Signed/authorized by patient. "
                "(*) Lacks capacity - signed by rep + clinician. "
                "(*) Under 16 - signed by 2/3 of (patient, clinician, "
                "parent); see special rules")


# =============================================================================
# Information about patient captured from clinical database
# =============================================================================

def to_date(d: Optional[Union[datetime.date,
                              datetime.datetime]]) -> Optional[datetime.date]:
    if isinstance(d, datetime.datetime):
        return d.date()
    return d  # datetime.date, or None


class ClinicianInfoHolder(object):
    CARE_COORDINATOR = 'care_coordinator'
    CONSULTANT = 'consultant'
    HCP = 'HCP'
    TEAM = 'team'

    def __init__(self, clinician_type: str,
                 title: str, first_name: str, surname: str, email: str,
                 signatory_title: str, is_consultant: bool,
                 start_date: Union[datetime.date, datetime.datetime],
                 end_date: Union[datetime.date, datetime.datetime],
                 address_components: List[str] = None) -> None:
        self.clinician_type = clinician_type
        self.title = title
        self.first_name = first_name
        self.surname = surname
        self.email = email or make_cpft_email_address(first_name, surname)
        self.signatory_title = signatory_title
        self.is_consultant = is_consultant
        self.start_date = to_date(start_date)
        self.end_date = to_date(end_date)
        self.address_components = address_components or []  # type: List[str]

        if clinician_type == self.CARE_COORDINATOR:
            self.clinician_preference_order = 1  # best
        elif clinician_type == self.CONSULTANT:
            self.clinician_preference_order = 2
        elif clinician_type == self.HCP:
            self.clinician_preference_order = 3
        elif clinician_type == self.TEAM:
            self.clinician_preference_order = 4
        else:
            self.clinician_preference_order = 99999  # worst

    def __repr__(self) -> str:
        return simple_repr(self, [
            'clinician_type',
            'title',
            'first_name',
            'surname',
            'email',
            'signatory_title',
            'is_consultant',
            'start_date',
            'end_date',
            'address_components',
        ])

    def current(self) -> bool:
        return self.end_date is None or self.end_date >= datetime.date.today()

    def contactable(self) -> bool:
        return bool(self.surname and self.email)


class PatientLookupBase(models.Model):
    """
    Base class for PatientLookup and DummyPatientSourceInfo.
    Must be able to be instantiate with defaults, for the "not found"
    situation.
    """

    MALE = 'M'
    FEMALE = 'F'
    INTERSEX = 'X'
    UNKNOWNSEX = '?'
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (INTERSEX, 'Inderminate/intersex'),
        (UNKNOWNSEX, 'Unknown'),
    )

    # Details of lookup
    pt_local_id_description = models.CharField(
        blank=True,
        max_length=LEN_FIELD_DESCRIPTION,
        verbose_name="Description of database-specific ID")
    pt_local_id_number = models.BigIntegerField(
        null=True, blank=True,
        verbose_name="Database-specific ID")
    # Information coming out: patient
    pt_dob = models.DateField(null=True, blank=True,
                              verbose_name="Patient date of birth")
    pt_dod = models.DateField(
        null=True, blank=True,
        verbose_name="Patient date of death (NULL if alive)")
    pt_dead = models.BooleanField(default=False,
                                  verbose_name="Patient is dead")
    pt_discharged = models.NullBooleanField(verbose_name="Patient discharged")
    pt_discharge_date = models.DateField(
        null=True, blank=True,
        verbose_name="Patient date of discharge")
    pt_sex = models.CharField(max_length=1, blank=True, choices=SEX_CHOICES,
                              verbose_name="Patient sex")
    pt_title = models.CharField(max_length=LEN_TITLE, blank=True,
                                verbose_name="Patient title")
    pt_first_name = models.CharField(max_length=LEN_NAME, blank=True,
                                     verbose_name="Patient first name")
    pt_last_name = models.CharField(max_length=LEN_NAME, blank=True,
                                    verbose_name="Patient last name")
    pt_address_1 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Patient address line 1")
    pt_address_2 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Patient address line 2")
    pt_address_3 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Patient address line 3")
    pt_address_4 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Patient address line 4")
    pt_address_5 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Patient address line 5 (county)")
    pt_address_6 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Patient address line 6 (postcode)")
    pt_address_7 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Patient address line 7 (country)")
    pt_telephone = models.CharField(max_length=LEN_PHONE, blank=True,
                                    verbose_name="Patient telephone")
    pt_email = models.EmailField(blank=True, verbose_name="Patient email")

    # Information coming out: GP
    gp_title = models.CharField(max_length=LEN_TITLE, blank=True,
                                verbose_name="GP title")
    gp_first_name = models.CharField(max_length=LEN_NAME, blank=True,
                                     verbose_name="GP first name")
    gp_last_name = models.CharField(max_length=LEN_NAME, blank=True,
                                    verbose_name="GP last name")
    gp_address_1 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="GP address line 1")
    gp_address_2 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="GP address line 2")
    gp_address_3 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="GP address line 3")
    gp_address_4 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="GP address line 4")
    gp_address_5 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="GP address line 5 (county)")
    gp_address_6 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="GP address line 6 (postcode)")
    gp_address_7 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="GP address line 7 (country)")
    gp_telephone = models.CharField(max_length=LEN_PHONE, blank=True,
                                    verbose_name="GP telephone")
    gp_email = models.EmailField(blank=True, verbose_name="GP email")

    # Information coming out: clinician
    clinician_title = models.CharField(max_length=LEN_TITLE, blank=True,
                                       verbose_name="Clinician title")
    clinician_first_name = models.CharField(
        max_length=LEN_NAME, blank=True,
        verbose_name="Clinician first name")
    clinician_last_name = models.CharField(
        max_length=LEN_NAME, blank=True,
        verbose_name="Clinician last name")
    clinician_address_1 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Clinician address line 1")
    clinician_address_2 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Clinician address line 2")
    clinician_address_3 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Clinician address line 3")
    clinician_address_4 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Clinician address line 4")
    clinician_address_5 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Clinician address line 5 (county)")
    clinician_address_6 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Clinician address line 6 (postcode)")
    clinician_address_7 = models.CharField(
        max_length=LEN_ADDRESS, blank=True,
        verbose_name="Clinician address line 7 (country)")
    clinician_telephone = models.CharField(max_length=LEN_PHONE, blank=True,
                                           verbose_name="Clinician telephone")
    clinician_email = models.EmailField(blank=True,
                                        verbose_name="Clinician email")
    clinician_is_consultant = models.BooleanField(
        default=False,
        verbose_name="Clinician is a consultant")
    clinician_signatory_title = models.CharField(
        max_length=LEN_NAME, blank=True,
        verbose_name="Clinician's title for signature "
                     "(e.g. 'Consultant psychiatrist')")

    class Meta:
        abstract = True

    # Generic title stuff:

    # -------------------------------------------------------------------------
    # Patient
    # -------------------------------------------------------------------------

    def pt_salutation(self) -> str:
        # noinspection PyTypeChecker
        return salutation(self.pt_title, self.pt_first_name, self.pt_last_name,
                          sex=self.pt_sex)

    def pt_title_forename_surname(self) -> str:
        # noinspection PyTypeChecker
        return title_forename_surname(self.pt_title, self.pt_first_name,
                                      self.pt_last_name)

    def pt_forename_surname(self) -> str:
        # noinspection PyTypeChecker
        return forename_surname(self.pt_first_name, self.pt_last_name)

    def pt_address_components(self) -> List[str]:
        return list(filter(None, [
            self.pt_address_1,
            self.pt_address_2,
            self.pt_address_3,
            self.pt_address_4,
            self.pt_address_5,
            self.pt_address_6,
            self.pt_address_7,
        ]))

    def pt_address_components_str(self) -> str:
        return ", ".join(filter(None, self.pt_address_components()))

    def pt_name_address_components(self) -> List[str]:
        return [
            self.pt_title_forename_surname()
        ] + self.pt_address_components()

    def get_id_numbers_html_bold(self) -> str:
        idnums = ["NHS#: {}".format(self.nhs_number)]
        if self.pt_local_id_description:
            idnums.append("{}: {}".format(self.pt_local_id_description,
                                          self.pt_local_id_number))
        return ". ".join(idnums)

    def get_pt_age_years(self) -> Optional[int]:
        if self.pt_dob is None:
            return None
        now = datetime.datetime.now()  # timezone-naive
        # now = timezone.now()  # timezone-aware
        return relativedelta(now, self.pt_dob).years

    def is_under_16(self) -> bool:
        age = self.get_pt_age_years()
        return age is not None and age < 16

    def is_under_15(self) -> bool:
        age = self.get_pt_age_years()
        return age is not None and age < 15

    def days_since_discharge(self) -> Optional[int]:
        """
        Returns days since discharge, or None if the patient is not
        discharged (or unknown).
        """
        if not self.pt_discharged or not self.pt_discharge_date:
            return None
        try:
            today = datetime.date.today()
            discharged = self.pt_discharge_date  # type: datetime.date
            diff = today - discharged
            return diff.days
        except (AttributeError, TypeError, ValueError):
            return None

    # -------------------------------------------------------------------------
    # GP
    # -------------------------------------------------------------------------

    def gp_title_forename_surname(self) -> str:
        return title_forename_surname(self.gp_title, self.gp_first_name,
                                      self.gp_last_name, always_title=True,
                                      assume_dr=True)

    def gp_address_components(self) -> List[str]:
        return list(filter(None, [
            self.gp_address_1,
            self.gp_address_2,
            self.gp_address_3,
            self.gp_address_4,
            self.gp_address_5,
            self.gp_address_6,
            self.gp_address_7,
        ]))

    def gp_address_components_str(self) -> str:
        return ", ".join(self.gp_address_components())

    def gp_name_address_str(self) -> str:
        return ", ".join(filter(None, [self.gp_title_forename_surname(),
                                       self.gp_address_components_str()]))

    # noinspection PyUnusedLocal
    def set_gp_name_components(self,
                               name: str,
                               decisions: List[str],
                               secret_decisions: List[str]) -> None:
        """
        Takes name, and stores it in the gp_title, gp_first_name, and
        gp_last_name fields.
        """
        secret_decisions.append(
            "Setting GP name components from: {}.".format(name))
        self.gp_title = ''
        self.gp_first_name = ''
        self.gp_last_name = ''
        if name == "No Registered GP" or not name:
            self.gp_last_name = "[No registered GP]"
            return
        if "(" in name:
            # A very odd thing like "LINTON H C (PL)"
            self.gp_last_name = name
            return
        (initial, surname) = get_initial_surname_tuple_from_string(name)
        initial = initial.title()
        surname = surname.title()
        self.gp_title = "Dr"
        self.gp_first_name = initial + ("." if initial else "")
        self.gp_last_name = surname

    # -------------------------------------------------------------------------
    # Clinician
    # -------------------------------------------------------------------------

    def clinician_salutation(self) -> str:
        # noinspection PyTypeChecker
        return salutation(self.clinician_title, self.clinician_first_name,
                          self.clinician_last_name, assume_dr=True)

    def clinician_title_forename_surname(self) -> str:
        # noinspection PyTypeChecker
        return title_forename_surname(self.clinician_title,
                                      self.clinician_first_name,
                                      self.clinician_last_name)

    def clinician_address_components(self) -> List[str]:
        # We're going to put the clinician's postal address into letters to
        # patients. Therefore, we need a sensible fallback, i.e. the RDBM's.
        address_components = [
            self.clinician_address_1,
            self.clinician_address_2,
            self.clinician_address_3,
            self.clinician_address_4,
            self.clinician_address_5,
            self.clinician_address_6,
            self.clinician_address_7,
        ]
        if not any(x for x in address_components):
            address_components = settings.RDBM_ADDRESS.copy()
            if address_components:
                address_components[0] = "c/o " + address_components[0]
        return list(filter(None, address_components))

    def clinician_address_components_str(self) -> str:
        return ", ".join(self.clinician_address_components())

    def clinician_name_address_str(self) -> str:
        return ", ".join(filter(None, [
            self.clinician_title_forename_surname(),
            self.clinician_address_components_str()]))

    # -------------------------------------------------------------------------
    # Paperwork
    # -------------------------------------------------------------------------

    def get_traffic_light_decision_form(self) -> str:
        context = {
            'patient_lookup': self,
            'settings': settings,
        }
        return render_pdf_html_to_string(
            'traffic_light_decision_form.html', context, patient=True)


class DummyPatientSourceInfo(PatientLookupBase):
    # Key
    nhs_number = models.BigIntegerField(verbose_name="NHS number",
                                        unique=True)

    class Meta:
        verbose_name_plural = "Dummy patient source information"

    def __str__(self):
        return (
            "[DummyPatientSourceInfo {}] "
            "Dummy patient lookup for NHS# {}".format(
                self.id,
                self.nhs_number))


class PatientLookup(PatientLookupBase):
    """
    Represents a moment of lookup up identifiable data about patient, GP,
    and clinician from the relevant clinical database.

    Inherits from DummyPatientSourceInfo so it has the same fields, and more.
    """

    DUMMY_CLINICAL = 'dummy_clinical'
    CPFT_PCMIS = 'cpft_pcmis'
    CPFT_CRS = 'cpft_crs'
    CPFT_RIO_RCEP = 'cpft_rio_rcep'
    CPFT_RIO_CRATE_PREPROCESSED = 'cpft_rio_crate'  # NB SOURCE_DB_NAME_MAX_LENGTH  # noqa
    DATABASE_CHOICES = (
        # First key must match a database entry in Django local settings.
        (DUMMY_CLINICAL, 'Dummy clinical database for testing'),
        # (CPFT_PCMIS, 'CPFT Psychological Wellbeing Service (IAPT) PC-MIS'),
        (CPFT_CRS, 'CPFT Care Records System (CRS) 2005-2012'),
        (CPFT_RIO_RCEP, 'CPFT RiO 2013- (preprocessed by Servelec RCEP tool)'),
        (CPFT_RIO_CRATE_PREPROCESSED, 'CPFT RiO 2013- (raw)'),
    )

    nhs_number = models.BigIntegerField(
        verbose_name="NHS number used for lookup")
    lookup_at = models.DateTimeField(
        verbose_name="When fetched from clinical database",
        auto_now_add=True)

    # Information going in
    source_db = models.CharField(
        max_length=SOURCE_DB_NAME_MAX_LENGTH, choices=DATABASE_CHOICES,
        verbose_name="Source database used for lookup")

    # Information coming out: general
    decisions = models.TextField(
        blank=True, verbose_name="Decisions made during lookup")
    secret_decisions = models.TextField(
        blank=True,
        verbose_name="Secret (identifying) decisions made during lookup")

    # Information coming out: patient
    pt_found = models.BooleanField(default=False, verbose_name="Patient found")

    # Information coming out: GP
    gp_found = models.BooleanField(default=False, verbose_name="GP found")

    # Information coming out: clinician
    clinician_found = models.BooleanField(default=False,
                                          verbose_name="Clinician found")

    def __repr__(self):
        return modelrepr(self)

    def __str__(self):
        return "[PatientLookup {}] NHS# {}".format(
            self.id,
            self.nhs_number,
        )

    def get_first_traffic_light_letter_html(self) -> str:
        """
        REC DOCUMENT 06. Covering letter to patient for first enquiry about
        research preference
        """
        context = {
            # Letter bits
            'address_from': self.clinician_address_components(),
            'address_to': self.pt_name_address_components(),
            'salutation': self.pt_salutation(),
            'signatory_name': self.clinician_title_forename_surname(),
            'signatory_title': self.clinician_signatory_title,
            # Specific bits
            'settings': settings,
            'patient_lookup': self,
        }
        return render_pdf_html_to_string(
            'letter_patient_first_traffic_light.html', context, patient=True)

    def set_from_clinician_info_holder(
            self, info: ClinicianInfoHolder) -> None:
        self.clinician_found = True
        self.clinician_title = info.title
        self.clinician_first_name = info.first_name
        self.clinician_last_name = info.surname
        self.clinician_email = info.email
        self.clinician_is_consultant = info.is_consultant
        self.clinician_signatory_title = info.signatory_title
        # Slice notation returns an empty list, rather than an exception,
        # if the index is out of range
        self.clinician_address_1 = info.address_components[0:1] or ''
        self.clinician_address_2 = info.address_components[1:2] or ''
        self.clinician_address_3 = info.address_components[2:3] or ''
        self.clinician_address_4 = info.address_components[3:4] or ''
        self.clinician_address_5 = info.address_components[4:5] or ''
        self.clinician_address_6 = info.address_components[5:6] or ''
        self.clinician_address_7 = info.address_components[6:7] or ''


APPROX_EMAIL_REGEX = re.compile(  # http://emailregex.com/
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def make_forename_surname_email_address(forename: str,
                                        surname: str,
                                        domain: str,
                                        default: str = '') -> str:
    if not forename or not surname:  # in case one is None
        return default
    forename = forename.replace(" ", "")
    surname = surname.replace(" ", "")
    if not forename or not surname:  # in case one is empty
        return default
    if len(forename) == 1:
        # Initial only; that won't do.
        return default
    # Other duff things we see: John Smith (CALT), where "Smith (CALT)" is the
    # surname and CALT is Cambridge Adult Locality Team. This can map to
    # something unpredictable, like JohnSmithOT@cpft.nhs.uk, so we can't use
    # it.
    # Formal definition is at http://stackoverflow.com/questions/2049502/what-characters-are-allowed-in-email-address  # noqa
    # See also: http://emailregex.com/
    attempt = "{}.{}@{}".format(forename, surname, domain)
    if APPROX_EMAIL_REGEX.match(attempt):
        return attempt
    else:
        return default


def make_cpft_email_address(forename: str, surname: str,
                            default: str = '') -> str:
    return make_forename_surname_email_address(forename, surname,
                                               "cpft.nhs.uk", default)


# =============================================================================
# Functions to do the patient lookups
# =============================================================================

def lookup_patient(nhs_number: int,
                   source_db: str = None,
                   save: bool = True,
                   existing_ok: bool = False) -> PatientLookup:
    source_db = source_db or settings.CLINICAL_LOOKUP_DB
    if source_db not in [x[0] for x in PatientLookup.DATABASE_CHOICES]:
        raise ValueError("Bad source_db: {}".format(source_db))
    if existing_ok:
        try:
            lookup = PatientLookup.objects.filter(nhs_number=nhs_number)\
                                          .latest('lookup_at')
            if lookup:
                return lookup
        except PatientLookup.DoesNotExist:
            # No existing lookup, so proceed to do it properly (below).
            pass
    lookup = PatientLookup(nhs_number=nhs_number,
                           source_db=source_db)
    decisions = []
    secret_decisions = []
    if source_db == PatientLookup.DUMMY_CLINICAL:
        lookup_dummy_clinical(lookup, decisions, secret_decisions)
    elif source_db == PatientLookup.CPFT_PCMIS:
        raise AssertionError("Don't know how to look up from PCMIS yet")
        # lookup_cpft_iapt(lookup, decisions, secret_decisions)
    elif source_db == PatientLookup.CPFT_CRS:
        lookup_cpft_crs(lookup, decisions, secret_decisions)
    elif source_db == PatientLookup.CPFT_RIO_RCEP:
        lookup_cpft_rio_rcep(lookup, decisions, secret_decisions)
    elif source_db == PatientLookup.CPFT_RIO_CRATE_PREPROCESSED:
        lookup_cpft_rio_crate_preprocessed(lookup, decisions, secret_decisions)
    else:
        raise AssertionError("Bug in lookup_patient")
    lookup.decisions = " ".join(decisions)
    lookup.secret_decisions = " ".join(secret_decisions)
    if save:
        lookup.save()
    return lookup


# -----------------------------------------------------------------------------
# Dummy clinical database (part of CRATE)
# -----------------------------------------------------------------------------

# noinspection PyUnusedLocal
def lookup_dummy_clinical(lookup: PatientLookup,
                          decisions: List[str],
                          secret_decisions: List[str]) -> None:
    try:
        dummylookup = DummyPatientSourceInfo.objects.get(
            nhs_number=lookup.nhs_number)
    except ObjectDoesNotExist:
        decisions.append("Patient not found in dummy lookup")
        return
    # noinspection PyProtectedMember
    fieldnames = [f.name for f in PatientLookupBase._meta.get_fields()]
    for fieldname in fieldnames:
        setattr(lookup, fieldname, getattr(dummylookup, fieldname))
    lookup.pt_found = True
    lookup.gp_found = True
    lookup.clinician_found = True
    decisions.append("Copying all information from dummy lookup")


# -----------------------------------------------------------------------------
# CPFT RiO (raw)
# -----------------------------------------------------------------------------

def lookup_cpft_rio_crate_preprocessed(lookup: PatientLookup,
                                       decisions: List[str],
                                       secret_decisions: List[str]) -> None:
    """
    Here, we use the version of RiO preprocessed by the CRATE preprocessor.
    This is almost identical to the RCEP version, saving us some thought and
    lots of repetition of complex JOIN code to deal with the raw RiO database.

    However, the CRATE preprocessor does this with views.
    We would need to index the underlying tables; however, the CRATE
    processor has also done this for us for the lookup tables, so we
    don't need so many.

    USE my_database_name;

    CREATE INDEX _idx_cdd_nhs ON ClientIndex (NNN);  -- already in RiO source

    CREATE INDEX _idx_cnh_id ON ClientName (ClientID);  -- already in RiO source  # noqa
    CREATE INDEX _idx_cnh_eff ON ClientName (EffectiveDate);  -- ignored
    CREATE INDEX _idx_cnh_end ON ClientName (EndDate);  -- ignored

    CREATE INDEX _idx_cah_id ON ClientAddress (ClientID);  -- already in RiO source as part of composite index  # noqa
    CREATE INDEX _idx_cah_from ON ClientAddress (FromDate);  -- ignored
    CREATE INDEX _idx_cah_to ON ClientAddress (ToDate);  -- ignored

    CREATE INDEX _idx_cch_id ON ClientTelecom (ClientID);  -- already in RiO source as part of composite index  # noqa

    CREATE INDEX _idx_cgh_id ON ClientHealthCareProvider (ClientID);  -- already in RiO source  # noqa
    CREATE INDEX _idx_cgh_from ON ClientHealthCareProvider (FromDate);  -- ignored  # noqa
    CREATE INDEX _idx_cgh_to ON ClientHealthCareProvider (ToDate);  -- ignored

    CREATE INDEX _idx_cc_id ON CPACareCoordinator (ClientID);  -- preprocessor adds this  # noqa
    CREATE INDEX _idx_cc_start ON CPACareCoordinator (StartDate);  -- ignored
    CREATE INDEX _idx_cc_end ON CPACareCoordinator (EndDate);  -- ignored

    CREATE INDEX _idx_ref_id ON AmsReferral (ClientID);  -- already in RiO source as part of composite index  # noqa
    CREATE INDEX _idx_ref_recv ON AmsReferral (ReferralReceivedDate);  -- ignored  # noqa
    CREATE INDEX _idx_ref_removal ON AmsReferral (RemovalDateTime);  -- ignored

    CREATE INDEX _idx_rsh_id ON AmsReferralAllocation (ClientID);  -- already in RiO source as part of composite index  # noqa
    CREATE INDEX _idx_rsh_start ON AmsReferralAllocation (StartDate);  -- ignored
    CREATE INDEX _idx_rsh_end ON AmsReferralAllocation (EndDate);  -- ignored

    CREATE INDEX _idx_rth_id ON AmsReferralTeam (ClientID);  -- already in RiO source as part of composite index  # noqa
    CREATE INDEX _idx_rth_start ON AmsReferralTeam (StartDate);  -- ignored
    CREATE INDEX _idx_rth_end ON AmsReferralTeam (EndDate);  -- ignored

    ... or alternative RiO number indexes on CRATE_COL_RIO_NUMBER field.

    Then, the only field name differences from RCEP are:

        Client_Name_History.End_Date  -- not End_Date_
    """
    lookup_cpft_rio_generic(lookup, decisions, secret_decisions,
                            as_crate_not_rcep=True)


# -----------------------------------------------------------------------------
# CPFT RiO as preprocessed by Servelec RCEP tool
# -----------------------------------------------------------------------------

def lookup_cpft_rio_rcep(lookup: PatientLookup,
                         decisions: List[str],
                         secret_decisions: List[str]) -> None:
    """
    ---------------------------------------------------------------------------
    RiO notes, 2015-05-19
    ... ADDENDUM 2017-02-27: this is the RiO database as modified by Servelec's
        RiO CRIS Extraction Program (RCEP). See also lookup_cpft_rio_raw().
    ---------------------------------------------------------------------------
    For speed, RiO-RCEP needs these indexes:

    USE my_database_name;

    CREATE INDEX _idx_cdd_nhs ON Client_Demographic_Details (NHS_Number);

    CREATE INDEX _idx_cnh_id ON Client_Name_History (Client_ID);
    CREATE INDEX _idx_cnh_eff ON Client_Name_History (Effective_Date);
    CREATE INDEX _idx_cnh_end ON Client_Name_History (End_Date_);

    CREATE INDEX _idx_cah_id ON Client_Address_History (Client_ID);
    CREATE INDEX _idx_cah_from ON Client_Address_History (Address_From_Date);
    CREATE INDEX _idx_cah_to ON Client_Address_History (Address_To_Date);

    CREATE INDEX _idx_cch_id ON Client_Communications_History (Client_ID);

    CREATE INDEX _idx_cgh_id ON Client_GP_History (Client_ID);
    CREATE INDEX _idx_cgh_from ON Client_GP_History (GP_From_Date);
    CREATE INDEX _idx_cgh_to ON Client_GP_History (GP_To_Date);

    CREATE INDEX _idx_cc_id ON CPA_CareCoordinator (Client_ID);
    CREATE INDEX _idx_cc_start ON CPA_CareCoordinator (Start_Date);
    CREATE INDEX _idx_cc_end ON CPA_CareCoordinator (End_Date);

    CREATE INDEX _idx_ref_id ON Main_Referral_Data (Client_ID);
    CREATE INDEX _idx_ref_recv ON Main_Referral_Data (Referral_Received_Date);
    CREATE INDEX _idx_ref_removal ON Main_Referral_Data (Removal_DateTime);

    CREATE INDEX _idx_rsh_id ON Referral_Staff_History (Client_ID);
    CREATE INDEX _idx_rsh_start ON Referral_Staff_History (Start_Date);
    CREATE INDEX _idx_rsh_end ON Referral_Staff_History (End_Date);

    CREATE INDEX _idx_rth_id ON Referral_Team_History (Client_ID);
    CREATE INDEX _idx_rth_start ON Referral_Team_History (Start_Date);
    CREATE INDEX _idx_rth_end ON Referral_Team_History (End_Date);

    -- CREATE INDEX _idx_rth_teamdesc ON Referral_Team_History (Team_Description);  # noqa
    """
    lookup_cpft_rio_generic(lookup, decisions, secret_decisions,
                            as_crate_not_rcep=False)


# -----------------------------------------------------------------------------
# CPFT RiO: function that copes with either the RCEP or the CRATE version,
# which are extremely similar.
# -----------------------------------------------------------------------------

def lookup_cpft_rio_generic(lookup: PatientLookup,
                            decisions: List[str],
                            secret_decisions: List[str],
                            as_crate_not_rcep: bool) -> None:
    """
    Main:
      Client_Demographic_Details
          Client_ID -- PK; RiO number; integer in VARCHAR(15) field
          Date_of_Birth -- DATETIME
          Date_of_Death -- DATETIME; NULL if not dead
          Death_Flag -- INT; 0 for alive, 1 for dead
          Deleted_Flag -- INT; 0 normally; 1 for deleted
          NHS_Number -- CHAR(10)
          Gender_Code -- 'F', 'M', 'U', 'X'
          Gender_Description -- 'Male', 'Female', ...

    Then, linked to it:

      Client_Name_History
          Client_ID -- integer in VARCHAR(15)
          Effective_Date -- DATETIME
          End_Date_  -- DATETIME, typically NULL
                -- in the CRATE version, this is End_Date instead
          Name_Type_Code  -- '1' for 'usual name', '2' for 'Alias', '3'
              for 'Preferred name', '4' for 'Birth name', '5' for
              'Maiden name', '7' for 'Other', 'CM' for 'Client Merge';
              NVARCHAR(10)
          Name_Type_Description  -- e.g. 'Usual name', 'Alias'
          Deleted_Flag -- INT

          title
          Given_Name_1  -- through to Given_Name_5
          Family_Name
          suffix
          ...

      Client_Address_History
          Client_ID -- integer in VARCHAR(15)
          Address_Type_Code -- e.g. 'PRIMARY' but also 'CA', 'FCH'...
          Address_Type_Description
          Address_From_Date -- DATETIME
          Address_To_Date -- DATETIME; NULL for active ones

          Address_Line_1
          Address_Line_2
          Address_Line_3
          Address_Line_4
          Address_Line_5
          Post_Code
          ... -- no e-mail address field

      Client_GP_History
          Client_ID -- integer in VARCHAR(15)
          GP_From_Date -- DATETIME
          GP_To_Date -- DATETIME; NULL for active ones

          GP_Name -- e.g. 'Smith JT'
          GP_Practice_Address_Line1
          GP_Practice_Address_Line2
          GP_Practice_Address_Line3
          GP_Practice_Address_Line4
          GP_Practice_Address_Line5
          GP_Practice_Post_code
          ...

    CPFT clinician details/?discharged info appear to be here:

      CPA_CareCoordinator
          Client_ID -- integer in VARCHAR(15)
          Start_Date -- DATETIME
          End_Date -- DATETIME
          End_Reason_Code
          End_Reason_Description
          End_Reason_National_Code

          Care_Coordinator_User_title
          Care_Coordinator_User_first_name
          Care_Coordinator_User_surname
          Care_Coordinator_User_email
          Care_Coordinator_User_Consultant_Flag -- INT; 0 or 1 (or NULL?)

      Main_Referral_Data
          Client_ID -- integer in VARCHAR(15)
          Referral_Received_Date -- DATETIME
          Removal_DateTime -- DATETIME
          # Care_Spell_Start_Date
          # Care_Spell_End_Date -- never non-NULL in our data set
          # Discharge_HCP -- ??user closing the referral

          Referred_Consultant_User_title
          Referred_Consultant_User_first_name
          Referred_Consultant_User_surname
          Referred_Consultant_User_email
          Referred_Consultant_User_Consultant_Flag  -- 0, 1, NULL

      Referral_Staff_History
          Client_ID -- integer in VARCHAR(15)
          Start_Date -- DATETIME
          End_Date -- DATETIME
          Current_At_Discharge -- INT -- ? -- 1 or NULL

          HCP_User_title
          HCP_User_first_name
          HCP_User_surname
          HCP_User_email
          HCP_User_Consultant_Flag  -- 0, 1, NULL

      Referral_Team_History
              -- similar, but for teams; no individual info
          Client_ID -- integer in VARCHAR(15)
          Start_Date -- DATETIME
          End_Date -- DATETIME
          Current_At_Discharge -- INT -- ? -- 1 or NULL

          Team_Code -- NVARCHAR -- e.g. 'TCGMH712'
          Team_Description -- NVARCHAR -- e.g. 'George Mackenzie'
          Team_Classification_Group_Code -- NVARCHAR -- e.g. 'FS'
          Team_Classification_Group_Description -- NVARCHAR -- e.g.
                                                          'Forensic Service'

    Not obviously relevant:

      Client_CPA -- records CPA start/end, etc.
      Client_Professional_Contacts -- empty table!

    Added 2017-02-27:

      Client_Communications_History -- email/phone
          Client_ID -- integer in VARCHAR(15)
          Method_Code -- NVARCHAR(10); '1' for 'Telephone number', '3'
              for 'Email address', '4' for 'Minicom/textphone number'
          Method_Description
          Context_Code -- e.g. '1' for 'Communication address at home',
              other codes for 'Vacation home...', etc.
          Context_Description
          Contact_Details -- NVARCHAR(80)

    """
    cursor = connections[lookup.source_db].cursor()
    rio_number_field = (CRATE_COL_RIO_NUMBER if as_crate_not_rcep
                        else RCEP_COL_PATIENT_ID)

    # -------------------------------------------------------------------------
    # RiO/RCEP: 1. Get RiO PK
    # -------------------------------------------------------------------------
    cursor.execute(
        """
            SELECT
                {rio_number_field}, -- RiO number (PK)
                -- NHS_Number,
                Date_of_Birth,
                Date_of_Death,
                Death_Flag,
                -- Deleted_Flag,
                Gender_Code
                -- Gender_Description,
            FROM Client_Demographic_Details
            WHERE
                NHS_Number = %s -- CHAR comparison
                AND (Deleted_Flag IS NULL OR Deleted_Flag = 0)
        """.format(rio_number_field=rio_number_field),
        [str(lookup.nhs_number)]
    )
    # Can't use "NOT Deleted_Flag" with SQL Server; you get
    # "An expression of non-boolean type specified in a context where a
    # condition is expected, near 'Deleted_Flag'."
    # The field is of type INTEGER NULL, but SQL Server won't auto-cast it
    # to something boolean.
    rows = dictfetchall(cursor)
    if not rows:
        decisions.append(
            "NHS number not found in Client_Demographic_Details table.")
        return
    if len(rows) > 1:
        decisions.append("Two patients found with that NHS number; aborting.")
        return
    row = rows[0]
    rio_client_id = row[rio_number_field]
    lookup.pt_local_id_description = "CPFT RiO number"
    lookup.pt_local_id_number = rio_client_id
    secret_decisions.append("RiO number: {}.".format(rio_client_id))
    lookup.pt_dob = to_date(row['Date_of_Birth'])
    lookup.pt_dod = to_date(row['Date_of_Death'])
    lookup.pt_dead = bool(lookup.pt_dod or row['Death_Flag'])
    lookup.pt_sex = "?" if row['Gender_Code'] == "U" else row['Gender_Code']

    # -------------------------------------------------------------------------
    # RiO/RCEP: 2. Name
    # -------------------------------------------------------------------------
    cursor.execute(
        """
            SELECT
                title,
                Given_Name_1,
                Family_Name
            FROM Client_Name_History
            WHERE
                {rio_number_field} = %s
                AND Effective_Date <= GETDATE()
                AND ({end_date_field} IS NULL OR {end_date_field} > GETDATE())
                AND (Deleted_Flag IS NULL OR Deleted_Flag = 0)
            ORDER BY Name_Type_Code
        """.format(
            rio_number_field=rio_number_field,
            end_date_field='End_Date' if as_crate_not_rcep else 'End_Date_',
        ),
        [rio_client_id]
    )
    row = dictfetchone(cursor)
    if not row:
        decisions.append(
            "No name/address information found in Client_Name_History.")
        return
    lookup.pt_found = True
    lookup.pt_title = row['title'] or ''
    lookup.pt_first_name = row['Given_Name_1'] or ''
    lookup.pt_last_name = row['Family_Name'] or ''
    # Deal with dodgy case
    lookup.pt_title = lookup.pt_title.title()
    lookup.pt_first_name = lookup.pt_first_name.title()
    lookup.pt_last_name = lookup.pt_last_name.title()

    # -------------------------------------------------------------------------
    # RiO/RCEP: 3. Address
    # -------------------------------------------------------------------------
    cursor.execute(
        """
            SELECT
                Address_Line_1,
                Address_Line_2,
                Address_Line_3,
                Address_Line_4,
                Address_Line_5,
                Post_Code
            FROM Client_Address_History
            WHERE
                {rio_number_field} = %s
                AND Address_From_Date <= GETDATE()
                AND (Address_To_Date IS NULL
                     OR Address_To_Date > GETDATE())
            ORDER BY CASE WHEN Address_Type_Code = 'PRIMARY' THEN '1'
                          ELSE Address_Type_Code END ASC
        """.format(rio_number_field=rio_number_field),
        [rio_client_id]
    )
    row = dictfetchone(cursor)
    if not row:
        decisions.append("No address found in Client_Address_History table.")
    else:
        lookup.pt_address_1 = row['Address_Line_1'] or ''
        lookup.pt_address_2 = row['Address_Line_2'] or ''
        lookup.pt_address_3 = row['Address_Line_3'] or ''
        lookup.pt_address_4 = row['Address_Line_4'] or ''
        lookup.pt_address_5 = row['Address_Line_5'] or ''
        lookup.pt_address_6 = row['Post_Code'] or ''

    # -------------------------------------------------------------------------
    # RiO/RCEP: 3b. Patient's e-mail address
    # -------------------------------------------------------------------------
    cursor.execute(
        """
            SELECT
                Contact_Details  -- an e-mail address if Method_Code = 3
            FROM Client_Communications_History
            WHERE
                {rio_number_field} = %s
                AND Method_Code = 3  -- e-mail address
                AND Valid_From <= GETDATE()
                AND (Valid_To IS NULL
                     OR Valid_To > GETDATE())
            ORDER BY Context_Code ASC
                -- 1 = Communication address at home
                -- 2 = Primary home (after business hours)
                -- 3 = Vacation home (when person on holiday)
                -- 4 = Office address
                -- 6 = Emergency contact
                -- 8 = Mobile device
        """.format(rio_number_field=rio_number_field),
        [rio_client_id]
    )
    rows = dictfetchall(cursor)
    if rows:
        row = rows[0]
        lookup.pt_email = row['Contact_Details']

    # -------------------------------------------------------------------------
    # RiO/RCEP: 4. GP
    # -------------------------------------------------------------------------
    if as_crate_not_rcep:
        cursor.execute(
            """
                SELECT
                    GP_Title,
                    GP_Forename,
                    GP_Surname,
                    GP_Practice_Address_Line_1,
                    GP_Practice_Address_Line_2,
                    GP_Practice_Address_Line_3,
                    GP_Practice_Address_Line_4,
                    GP_Practice_Address_Line_5,
                    GP_Practice_Post_Code
                FROM Client_GP_History
                WHERE
                    {rio_number_field} = %s
                    AND GP_From_Date <= GETDATE()
                    AND (GP_To_Date IS NULL OR GP_To_Date > GETDATE())
            """.format(rio_number_field=rio_number_field),
            [rio_client_id]
        )
        row = dictfetchone(cursor)
        if not row:
            decisions.append("No GP found in Client_GP_History table.")
        else:
            lookup.gp_found = True
            lookup.gp_title = row['GP_Title'] or 'Dr'
            lookup.gp_first_name = row['GP_Forename'] or ''
            lookup.gp_last_name = row['GP_Surname'] or ''
            lookup.gp_address_1 = row['GP_Practice_Address_Line_1'] or ''
            lookup.gp_address_2 = row['GP_Practice_Address_Line_2'] or ''
            lookup.gp_address_3 = row['GP_Practice_Address_Line_3'] or ''
            lookup.gp_address_4 = row['GP_Practice_Address_Line_4'] or ''
            lookup.gp_address_5 = row['GP_Practice_Address_Line_5'] or ''
            lookup.gp_address_6 = row['GP_Practice_Post_Code']
    else:
        cursor.execute(
            """
                SELECT
                    GP_Name,
                    GP_Practice_Address_Line1,
                    GP_Practice_Address_Line2,
                    GP_Practice_Address_Line3,
                    GP_Practice_Address_Line4,
                    GP_Practice_Address_Line5,
                    GP_Practice_Post_code
                FROM Client_GP_History
                WHERE
                    {rio_number_field} = %s
                    AND GP_From_Date <= GETDATE()
                    AND (GP_To_Date IS NULL OR GP_To_Date > GETDATE())
            """.format(rio_number_field=rio_number_field),
            [rio_client_id]
        )
        row = dictfetchone(cursor)
        if not row:
            decisions.append("No GP found in Client_GP_History table.")
        else:
            lookup.gp_found = True
            lookup.set_gp_name_components(row['GP_Name'] or '',
                                          decisions, secret_decisions)
            lookup.gp_address_1 = row['GP_Practice_Address_Line1'] or ''
            lookup.gp_address_2 = row['GP_Practice_Address_Line2'] or ''
            lookup.gp_address_3 = row['GP_Practice_Address_Line3'] or ''
            lookup.gp_address_4 = row['GP_Practice_Address_Line4'] or ''
            lookup.gp_address_5 = row['GP_Practice_Address_Line5'] or ''
            lookup.gp_address_6 = row['GP_Practice_Post_code']

    # -------------------------------------------------------------------------
    # RiO/RCEP: 5. Clinician, active v. discharged
    # -------------------------------------------------------------------------
    # This bit is complicated! We do it last, so we can return upon success.
    clinicians = []  # type: List[ClinicianInfoHolder]
    #
    # (a) Care coordinator?
    #
    if as_crate_not_rcep:
        care_co_title_field = 'Care_Coordinator_Title'
        care_co_forename_field = 'Care_Coordinator_First_Name'
        care_co_surname_field = 'Care_Coordinator_Surname'
        care_co_email_field = 'Care_Coordinator_Email'
        care_co_consultant_flag_field = 'Care_Coordinator_Consultant_Flag'
        care_co_table = 'CPA_Care_Coordinator'
    else:
        care_co_title_field = 'Care_Coordinator_User_title'
        care_co_forename_field = 'Care_Coordinator_User_first_name'
        care_co_surname_field = 'Care_Coordinator_User_surname'
        care_co_email_field = 'Care_Coordinator_User_email'
        care_co_consultant_flag_field = 'Care_Coordinator_User_Consultant_Flag'
        care_co_table = 'CPA_CareCoordinator'
    cursor.execute(
        """
            SELECT
                {care_co_title_field},
                {care_co_forename_field},
                {care_co_surname_field},
                {care_co_email_field},
                {care_co_consultant_flag_field},
                Start_Date,
                End_Date
            FROM {care_co_table}
            WHERE
                {rio_number_field} = %s
                AND Start_Date <= GETDATE()
        """.format(
            care_co_title_field=care_co_title_field,
            care_co_forename_field=care_co_forename_field,
            care_co_surname_field=care_co_surname_field,
            care_co_email_field=care_co_email_field,
            care_co_consultant_flag_field=care_co_consultant_flag_field,
            care_co_table=care_co_table,
            rio_number_field=rio_number_field,
        ),
        [rio_client_id]
    )
    for row in dictfetchall(cursor):
        clinicians.append(ClinicianInfoHolder(
            clinician_type=ClinicianInfoHolder.CARE_COORDINATOR,
            title=row[care_co_title_field] or '',
            first_name=row[care_co_forename_field] or '',
            surname=row[care_co_surname_field] or '',
            email=row[care_co_email_field] or '',
            signatory_title="Care coordinator",
            is_consultant=bool(row[care_co_consultant_flag_field]),
            start_date=row['Start_Date'],
            end_date=row['End_Date'],
        ))
    #
    # (b) Active named consultant referral?
    #
    if as_crate_not_rcep:
        cons_title_field = 'Referred_Consultant_Title'
        cons_forename_field = 'Referred_Consultant_First_Name'
        cons_surname_field = 'Referred_Consultant_Surname'
        cons_email_field = 'Referred_Consultant_Email'
        cons_consultant_flag_field = 'Referred_Consultant_Consultant_Flag'
        referral_table = 'Referral'
    else:
        cons_title_field = 'Referred_Consultant_User_title'
        cons_forename_field = 'Referred_Consultant_User_first_name'
        cons_surname_field = 'Referred_Consultant_User_surname'
        cons_email_field = 'Referred_Consultant_User_email'
        cons_consultant_flag_field = 'Referred_Consultant_User_Consultant_Flag'
        referral_table = 'Main_Referral_Data'
    cursor.execute(
        """
            SELECT
                {cons_title_field},
                {cons_forename_field},
                {cons_surname_field},
                {cons_email_field},
                {cons_consultant_flag_field},
                Referral_Received_Date,
                Removal_DateTime
            FROM {referral_table}
            WHERE
                {rio_number_field} = %s
                AND Referral_Received_Date <= GETDATE()
        """.format(
            cons_title_field=cons_title_field,
            cons_forename_field=cons_forename_field,
            cons_surname_field=cons_surname_field,
            cons_email_field=cons_email_field,
            cons_consultant_flag_field=cons_consultant_flag_field,
            referral_table=referral_table,
            rio_number_field=rio_number_field,
        ),
        [rio_client_id]
    )
    for row in dictfetchall(cursor):
        clinicians.append(ClinicianInfoHolder(
            clinician_type=ClinicianInfoHolder.CONSULTANT,
            title=row[cons_title_field] or '',
            first_name=row[cons_forename_field] or '',
            surname=row[cons_surname_field] or '',
            email=row[cons_email_field] or '',
            signatory_title="Consultant psychiatrist",
            is_consultant=bool(row[cons_consultant_flag_field]),
            # ... would be odd if this were not true!
            start_date=row['Referral_Received_Date'],
            end_date=row['Removal_DateTime'],
        ))
    #
    # (c) Active other named staff referral?
    #
    if as_crate_not_rcep:
        hcp_title_field = 'HCP_Title'
        hcp_forename_field = 'HCP_First_Name'
        hcp_surname_field = 'HCP_Surname'
        hcp_email_field = 'HCP_Email'
        hcp_consultant_flag_field = 'HCP_Consultant_Flag'
    else:
        hcp_title_field = 'HCP_User_title'
        hcp_forename_field = 'HCP_User_first_name'
        hcp_surname_field = 'HCP_User_surname'
        hcp_email_field = 'HCP_User_email'
        hcp_consultant_flag_field = 'HCP_User_Consultant_Flag'
    cursor.execute(
        """
            SELECT
                {hcp_title_field},
                {hcp_forename_field},
                {hcp_surname_field},
                {hcp_email_field},
                {hcp_consultant_flag_field},
                Start_Date,
                End_Date
            FROM Referral_Staff_History
            WHERE
                {rio_number_field} = %s
                AND Start_Date <= GETDATE()
        """.format(
            hcp_title_field=hcp_title_field,
            hcp_forename_field=hcp_forename_field,
            hcp_surname_field=hcp_surname_field,
            hcp_email_field=hcp_email_field,
            hcp_consultant_flag_field=hcp_consultant_flag_field,
            rio_number_field=rio_number_field,
        ),
        [rio_client_id]
    )
    for row in dictfetchall(cursor):
        clinicians.append(ClinicianInfoHolder(
            clinician_type=ClinicianInfoHolder.HCP,
            title=row[hcp_title_field] or '',
            first_name=row[hcp_forename_field] or '',
            surname=row[hcp_surname_field] or '',
            email=row[hcp_email_field] or '',
            signatory_title="Clinician",
            is_consultant=bool(row[hcp_consultant_flag_field]),
            start_date=row['Start_Date'],
            end_date=row['End_Date'],
        ))
    #
    # (d) Active team referral?
    #
    cursor.execute(
        """
            SELECT
                Team_Description,
                Start_Date,
                End_Date
            FROM Referral_Team_History
            WHERE
                {rio_number_field} = %s
                AND Start_Date <= GETDATE()
        """.format(rio_number_field=rio_number_field),
        [rio_client_id]
    )
    for row in dictfetchall(cursor):
        team_info = ClinicianInfoHolder(
            clinician_type=ClinicianInfoHolder.TEAM,
            title='',
            first_name='',
            surname='',
            email='',
            signatory_title="Clinical team member",
            is_consultant=False,
            start_date=row['Start_Date'],
            end_date=row['End_Date'],
        )
        # We know a team - do we have a team representative?
        team_description = row['Team_Description']
        team_summary = "{status} team {desc}".format(
            status="active" if team_info.end_date is None else "previous",
            desc=repr(team_description),
        )
        try:
            teamrep = TeamRep.objects.get(team=team_description)
            decisions.append("Clinical team representative found.")
            profile = teamrep.user.profile
            team_info.title = profile.title
            team_info.first_name = teamrep.user.first_name
            team_info.surname = teamrep.user.last_name
            team_info.email = teamrep.user.email
            team_info.signatory_title = profile.signatory_title
            team_info.is_consultant = profile.is_consultant
        except ObjectDoesNotExist:
            decisions.append("No team representative found for "
                             "{}.".format(team_summary))
        except MultipleObjectsReturned:
            decisions.append("Confused: >1 team representative found for "
                             "{}.".format(team_summary))
        clinicians.append(team_info)
        # We append it even if we can't find a representative, because it still
        # carries information about whether the patient is discharged or not.

    # Re CLINICIAN ADDRESSES:
    # Candidate tables in RiO:
    # - OrgContactAddress +/- OrgContactAddressHistory
    # - OrgOrganisation
    # - GenPerson <-- THIS. From GenHCP: "This table contains about all HCPs
    #   registered in RiO. HCP’s personal details (name, address etc.) are
    #   stored in GenPerson.
    # - ??GenLocation; ??GenNHSLocation
    #
    # So, GenPerson is correct. However, in CPFT, when we
    #       SELECT * FROM GenPerson WHERE AddressLine2 IS NOT NULL
    # we get lots of things saying "Agency Staff", "leaves Trust 17/02/15",
    # "changed name from Smith", "Medical student", and so on.
    #
    # Therefore, our source is simply duff; people are using the fields for
    # a different purpose.
    # Therefore, the set_from_clinician_info_holder() function will default
    # to the RDBM's address.

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # OK.
    # Now we know all relevant recent clinicians, including (potentially) ones
    # from which the patient has been discharged, and ones that are active.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    decisions.append(
        "{} total past/present clinician(s)/team(s) found: {}.".format(
            len(clinicians), repr(clinicians)))
    current_clinicians = [c for c in clinicians if c.current()]
    if current_clinicians:
        lookup.pt_discharged = False
        lookup.pt_discharge_date = None
        decisions.append("Patient not discharged.")
        contactable_curr_clin = [c for c in current_clinicians
                                 if c.contactable()]
        # Sorting by two keys: http://stackoverflow.com/questions/11206884
        # LOW priority: most recent clinician. (Goes first in sort.)
        # HIGH priority: preferred type of clinician. (Goes last in sort.)
        # Sort order is: most preferred first.
        contactable_curr_clin.sort(key=attrgetter('start_date'), reverse=True)
        contactable_curr_clin.sort(key=attrgetter('clinician_preference_order'))  # noqa
        decisions.append("{} contactable active clinician(s) found.".format(
            len(contactable_curr_clin)))
        if contactable_curr_clin:
            chosen_clinician = contactable_curr_clin[0]
            lookup.set_from_clinician_info_holder(chosen_clinician)
            decisions.append("Found active clinician of type: {}".format(
                chosen_clinician.clinician_type))
            return  # All done!
        # If we get here, the patient is not discharged, but we haven't found
        # a contactable active clinician.
        # We'll fall through and check older clinicians for contactability.
    else:
        end_dates = [c.end_date for c in clinicians]
        lookup.pt_discharged = True
        lookup.pt_discharge_date = latest_date(*end_dates)
        decisions.append("Patient discharged.")

    # We get here either if the patient is discharged, or they're current but
    # we can't contact a current clinician.
    contactable_old_clin = [c for c in clinicians if c.contactable()]
    # LOW priority: preferred type of clinician. (Goes first in sort.)
    # HIGH priority: most recent end date. (Goes last in sort.)
    # Sort order is: most preferred first.
    contactable_old_clin.sort(key=attrgetter('clinician_preference_order'))
    contactable_old_clin.sort(key=attrgetter('end_date'), reverse=True)
    decisions.append("{} contactable previous clinician(s) found.".format(
        len(contactable_old_clin)))
    if contactable_old_clin:
        chosen_clinician = contactable_old_clin[0]
        lookup.set_from_clinician_info_holder(chosen_clinician)
        decisions.append("Found previous clinician of type: {}".format(
            chosen_clinician.clinician_type))

    if not lookup.clinician_found:
        decisions.append("Failed to establish contactable clinician.")


# -----------------------------------------------------------------------------
# CPFT Care Records System (CRS)
# -----------------------------------------------------------------------------

def lookup_cpft_crs(lookup, decisions, secret_decisions):
    cursor = connections[lookup.source_db].cursor()
    # -------------------------------------------------------------------------
    # CRS 1. Fetch basic details
    # -------------------------------------------------------------------------
    # Incoming nhs_number will be a number. However, the database has a VARCHAR
    # field (nhs_identifier) that may include spaces. So we compare a
    # whitespace-stripped field to our value converted to a VARCHAR:
    #       WHERE REPLACE(nhs_identifier, ' ', '') = CAST(%s AS VARCHAR)
    # ... or the other way round:
    #       WHERE CAST(nhs_identifier AS BIGINT) = %s
    cursor.execute(
        """
            SELECT
                patient_id, -- M number (PK)
                -- nhs_identifier,
                title,
                forename,
                surname,
                gender,
                -- ethnicity,
                -- marital_status,
                -- religion,
                dttm_of_birth,
                dttm_of_death
            FROM mpi
            WHERE CAST(nhs_identifier AS BIGINT) = %s
        """,
        [lookup.nhs_number]
    )
    rows = dictfetchall(cursor)
    if not rows:
        decisions.append("NHS number not found in mpi table.")
        return
    if len(rows) > 1:
        decisions.append("Two patients found with that NHS number; aborting.")
        return
    row = rows[0]
    crs_patient_id = row['patient_id']
    lookup.pt_local_id_description = "CPFT M number"
    lookup.pt_local_id_number = crs_patient_id
    secret_decisions.append("CPFT M number: {}.".format(crs_patient_id))
    lookup.pt_found = True
    lookup.pt_title = row['title'] or ''
    lookup.pt_first_name = row['forename'] or ''
    lookup.pt_last_name = row['surname'] or ''
    lookup.pt_sex = row['gender'] or ''
    lookup.pt_dob = row['dttm_of_birth']
    lookup.pt_dod = row['dttm_of_death']
    lookup.pt_dead = bool(lookup.pt_dod)
    # Deal with dodgy case
    lookup.pt_title = lookup.pt_title.title()
    lookup.pt_first_name = lookup.pt_first_name.title()
    lookup.pt_last_name = lookup.pt_last_name.title()
    # -------------------------------------------------------------------------
    # CRS 2. Address
    # -------------------------------------------------------------------------
    cursor.execute(
        """
            SELECT
                -- document_id, -- PK
                address1,
                address2,
                address3,
                address4,
                postcode,
                email
                -- startdate
                -- enddate
                -- patient_id

            FROM Address
            WHERE
                patient_id = %s
                AND enddate IS NULL
        """,
        [crs_patient_id]
    )
    row = dictfetchone(cursor)
    if not row:
        decisions.append("No address found in Address table.")
    else:
        lookup.pt_address_1 = row['address1'] or ''
        lookup.pt_address_2 = row['address2'] or ''
        lookup.pt_address_3 = row['address3'] or ''
        lookup.pt_address_4 = row['address4'] or ''
        lookup.pt_address_6 = row['postcode'] or ''
        lookup.pt_email = row['email'] or ''
    # -------------------------------------------------------------------------
    # CRS 3. GP
    # -------------------------------------------------------------------------
    cursor.execute(
        """
            SELECT
                -- sourcesystempk,  # PK
                -- patient_id,  # FK
                -- national_gp_id,
                gpname,
                -- national_practice_id,
                practicename,
                address1,
                address2,
                address3,
                address4,
                address5,
                postcode,
                telno
                -- startdate,
                -- enddate,
            FROM PracticeGP
            WHERE
                patient_id = %s
                AND enddate IS NULL
        """,
        [crs_patient_id]
    )
    row = dictfetchone(cursor)
    if not row:
        decisions.append("No GP found in PracticeGP table.")
    else:
        lookup.gp_found = True
        lookup.set_gp_name_components(row['gpname'] or '',
                                      decisions, secret_decisions)
        lookup.gp_address_1 = row['practicename'] or ''
        lookup.gp_address_2 = row['address1'] or ''
        lookup.gp_address_3 = row['address2'] or ''
        lookup.gp_address_4 = row['address3'] or ''
        lookup.gp_address_5 = ", ".join([row['address4'] or '',
                                         row['address5'] or ''])
        lookup.gp_address_6 = row['postcode']
        lookup.gp_telephone = row['telno']
    # -------------------------------------------------------------------------
    # CRS 4. Clinician
    # -------------------------------------------------------------------------
    cursor.execute(
        """
            SELECT
                -- patient_id,  # PK
                -- trustarea,
                consultanttitle,
                consultantfirstname,
                consultantlastname,
                carecoordinatortitle,
                carecoordinatorfirstname,
                carecoordinatorlastname,
                carecoordinatoraddress1,
                carecoordinatoraddress2,
                carecoordinatoraddress3,
                carecoordinatortown,
                carecoordinatorcounty,
                carecoordinatorpostcode,
                carecoordinatoremailaddress,
                carecoordinatormobilenumber,
                carecoordinatorlandlinenumber
            FROM CDLPatient
            WHERE
                patient_id = %s
        """,
        [crs_patient_id]
    )
    row = dictfetchone(cursor)
    if not row:
        decisions.append("No clinician info found in CDLPatient table.")
    else:
        lookup.clinician_address_1 = row['carecoordinatoraddress1'] or ''
        lookup.clinician_address_2 = row['carecoordinatoraddress2'] or ''
        lookup.clinician_address_3 = row['carecoordinatoraddress3'] or ''
        lookup.clinician_address_4 = row['carecoordinatortown'] or ''
        lookup.clinician_address_5 = row['carecoordinatorcounty'] or ''
        lookup.clinician_address_6 = row['carecoordinatorpostcode'] or ''
        lookup.clinician_telephone = " / ".join([
            row['carecoordinatorlandlinenumber'] or '',
            row['carecoordinatormobilenumber'] or ''
        ])
        careco_email = (
            row['carecoordinatoremailaddress'] or
            make_cpft_email_address(row['carecoordinatorfirstname'],
                                    row['carecoordinatorlastname'])
        )
        cons_email = make_cpft_email_address(row['consultantfirstname'],
                                             row['consultantlastname'])
        if careco_email:
            # Use care coordinator information
            lookup.clinician_found = True
            lookup.clinician_title = row['carecoordinatortitle'] or ''
            lookup.clinician_first_name = row['carecoordinatorfirstname'] or ''
            lookup.clinician_last_name = row['carecoordinatorlastname'] or ''
            lookup.clinician_email = careco_email
            lookup.clinician_signatory_title = "Care coordinator"
            decisions.append("Clinician found: care coordinator (CDL).")
        elif cons_email:
            # Use consultant information
            lookup.clinician_found = True
            lookup.clinician_title = row['consultanttitle'] or ''
            lookup.clinician_first_name = row['consultantfirstname'] or ''
            lookup.clinician_last_name = row['consultantlastname'] or ''
            lookup.clinician_email = cons_email
            lookup.clinician_signatory_title = "Consultant psychiatrist"
            lookup.clinician_is_consultant = True
            decisions.append("Clinician found: consultant psychiatrist (CDL).")
        else:
            # Don't know
            decisions.append(
                "No/insufficient clinician information found (CDL).")


# =============================================================================
# Clinical team representative
# =============================================================================

class TeamInfo(object):
    """Class only exists to be able to use @cached_property."""
    @cached_property
    def teams(self):
        log.debug("Fetching/caching clinical teams")
        if settings.CLINICAL_LOOKUP_DB in (PatientLookup.CPFT_RIO_RCEP,
                                           PatientLookup.CPFT_RIO_CRATE_PREPROCESSED):  # noqa
            cursor = connections[settings.CLINICAL_LOOKUP_DB].cursor()
            cursor.execute("""
                SELECT DISTINCT Team_Description
                FROM Referral_Team_History
                ORDER BY Team_Description
            """)
            return fetchallfirstvalues(cursor)
        elif settings.CLINICAL_LOOKUP_DB == 'dummy_clinical':
            return ["dummy_team_one", "dummy_team_two", "dummy_team_three"]
        else:
            return []

    @cached_property
    def team_choices(self) -> List[Tuple[str, str]]:
        teams = self.teams
        return [(team, team) for team in teams]


all_teams_info = TeamInfo()


class TeamRep(models.Model):
    team = models.CharField(max_length=LEN_NAME, unique=True,
                            choices=all_teams_info.team_choices,
                            verbose_name="Team description")
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = "clinical team representative"
        verbose_name_plural = "clinical team representatives"


# =============================================================================
# Record of payments to charity
# =============================================================================
# In passing - singleton objects:
#   http://goodcode.io/articles/django-singleton-models/

class CharityPaymentRecord(models.Model):
    created_at = models.DateTimeField(verbose_name="When created",
                                      auto_now_add=True)
    payee = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)


# =============================================================================
# Record of consent mode for a patient
# =============================================================================

class ConsentMode(Decision):
    RED = 'red'
    YELLOW = 'yellow'
    GREEN = 'green'

    CONSENT_MODE_CHOICES = (
        (RED, 'red'),
        (YELLOW, 'yellow'),
        (GREEN, 'green'),
    )
    # ... http://stackoverflow.com/questions/12822847/best-practice-for-python-django-constants  # noqa

    SOURCE_USER_ENTRY = "crate_user_entry"
    SOURCE_AUTOCREATED = "crate_auto_created"
    SOURCE_LEGACY = "legacy"  # default, for old versions

    nhs_number = models.BigIntegerField(verbose_name="NHS number")
    current = models.BooleanField(default=False)
    # see save() and process_change() below
    created_at = models.DateTimeField(
        verbose_name="When was this record created?",
        auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    exclude_entirely = models.BooleanField(
        default=False,
        verbose_name="Exclude patient from Research Database entirely?")
    consent_mode = models.CharField(
        max_length=10, default="", choices=CONSENT_MODE_CHOICES,
        verbose_name="Consent mode (red/yellow/green)")
    consent_after_discharge = models.BooleanField(
        default=False,
        verbose_name="Consent given to contact patient after discharge?")
    max_approaches_per_year = models.PositiveSmallIntegerField(
        verbose_name="Maximum number of approaches permissible per year "
                     "(0 = no limit)",
        default=0)
    other_requests = models.TextField(
        blank=True,
        verbose_name="Other special requests by patient")
    prefers_email = models.BooleanField(
        default=False,
        verbose_name="Patient prefers e-mail contact?")
    changed_by_clinician_override = models.BooleanField(
        default=False,
        verbose_name="Consent mode changed by clinician's override?")

    source = models.CharField(
        max_length=SOURCE_DB_NAME_MAX_LENGTH,
        default=SOURCE_USER_ENTRY,
        verbose_name="Source of information")

    # class Meta:
    #     get_latest_by = "created_at"

    def save(self, *args, **kwargs) -> None:
        """
        Custom save method.
        Ensures that only one Query has active == True for a given user.

        Better than a get_latest_by clause, because with a flag like this, we
        can have a simple query that says "get the current records for all
        patients" -- harder if done by date (group by patient, order by
        patient/date, pick last one for each patient...).
        """
        # http://stackoverflow.com/questions/1455126/unique-booleanfield-value-in-django  # noqa
        if self.current:
            ConsentMode.objects\
                       .filter(nhs_number=self.nhs_number, current=True)\
                       .update(current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return "[ConsentMode {}] NHS# {}, {}".format(
            self.id,
            self.nhs_number,
            self.consent_mode,
        )

    @classmethod
    def get_or_create(
            cls,
            nhs_number: int,
            created_by: settings.AUTH_USER_MODEL) -> CONSENT_MODE_FWD_REF:
        """
        Fetches the current ConsentMode for this patient.
        If there isn't one, creates a default one and returns that.
        """
        try:
            consent_mode = cls.objects.get(nhs_number=nhs_number,
                                           current=True)
        except cls.DoesNotExist:
            consent_mode = cls(nhs_number=nhs_number,
                               created_by=created_by,
                               source=cls.SOURCE_AUTOCREATED,
                               current=True)
            consent_mode.save()
        except cls.MultipleObjectsReturned:
            log.warning("bug: ConsentMode.get_or_create() received "
                        "exception ConsentMode.MultipleObjectsReturned")
            consent_mode = cls(nhs_number=nhs_number,
                               created_by=created_by,
                               source=cls.SOURCE_AUTOCREATED,
                               current=True)
            consent_mode.save()
        return consent_mode

    #*** remove when we do something here:
    # noinspection PyUnusedLocal
    @classmethod
    def refresh_from_primary_clinical_record(
            cls,
            nhs_number: int,
            created_by: settings.AUTH_USER_MODEL,
            source_db: str = None) -> None:
        """
        Checks the primary clinical record and CRATE's own records for consent
        modes for this patient. If the most recent one is in the external
        database, copies it to CRATE's database and marks that one as current.

        This has the effect that external primary clinical records (e.g. RiO)
        take priority, but if there's no record in RiO, we can still proceed.
        """
        source_db = source_db or settings.CLINICAL_LOOKUP_DB
        if source_db not in [x[0] for x in PatientLookup.DATABASE_CHOICES]:
            raise ValueError("Bad source_db: {}".format(source_db))
        if source_db != PatientLookup.CPFT_RIO_CRATE_PREPROCESSED:
            # Don't know how to look up consent modes from other sources
            return
        pass # *** implement consent-mode lookup when RiO updated
        # Will need to:
        # - Fetch the most recent record.
        # - If its date is later than the most recent CRATE record:
        #   - create a new ConsentMode with (..., source=source_db)
        #   - save it

    def consider_withdrawal(self) -> None:
        """
        If required, withdraw consent for other studies.
        Call this before setting current=True and calling save().
        Note that as per Major Amendment 1 to 12/EE/0407, this happens
        automatically, rather than having a special flag to control it.
        """
        try:
            previous = ConsentMode.objects.get(
                nhs_number=self.nhs_number,
                current=True)
            if (previous.consent_mode == ConsentMode.GREEN and
                    self.consent_mode != ConsentMode.GREEN):
                contact_requests = (
                    ContactRequest.objects
                    .filter(nhs_number=self.nhs_number)
                    .filter(consent_mode__consent_mode=ConsentMode.GREEN)
                    .filter(decided_send_to_researcher=True)
                    .filter(consent_withdrawn=False)
                )
                for contact_request in contact_requests:
                    (letter,
                     email_succeeded) = contact_request.withdraw_consent()
                    if not email_succeeded:
                        self.notify_rdbm_of_work(letter, to_researcher=True)
        except ConsentMode.DoesNotExist:
            pass  # no previous ConsentMode; nothing to do.
        except ConsentMode.MultipleObjectsReturned:
            log.warning("bug: ConsentMode.consider_withdrawal() received "
                        "exception ConsentMode.MultipleObjectsReturned")
            # do nothing else

    def get_latest_patient_lookup(self) -> PatientLookup:
        # noinspection PyTypeChecker
        return lookup_patient(self.nhs_number, existing_ok=True)

    def get_confirm_traffic_to_patient_letter_html(self) -> str:
        """
        REC DOCUMENT 07. Confirming patient's traffic-light choice.
        """
        patient_lookup = self.get_latest_patient_lookup()
        context = {
            # Letter bits
            'address_from': settings.RDBM_ADDRESS + [settings.RDBM_EMAIL],
            'address_to': patient_lookup.pt_name_address_components(),
            'salutation': patient_lookup.pt_salutation(),
            'signatory_name': settings.RDBM_NAME,
            'signatory_title': settings.RDBM_TITLE,
            # Specific bits
            'consent_mode': self,
            'patient_lookup': patient_lookup,
            'settings': settings,
            # URLs
            'red_img_url': site_absolute_url(static('red.png')),
            'yellow_img_url': site_absolute_url(static('yellow.png')),
            'green_img_url': site_absolute_url(static('green.png')),
        }
        # 1. Building a static URL in code:
        #    http://stackoverflow.com/questions/11721818/django-get-the-static-files-url-in-view  # noqa
        # 2. Making it an absolute URL means that wkhtmltopdf will also see it
        #    (by fetching it from this web server).
        # 3. Works with Django testing server.
        # 4. Works with Apache, + proxying to backend, + SSL
        return render_pdf_html_to_string('letter_patient_confirm_traffic.html',
                                         context, patient=True)

    def notify_rdbm_of_work(self,
                            letter: LETTER_FWD_REF,
                            to_researcher: bool = False) -> None:
        subject = ("WORK FROM RESEARCH DATABASE COMPUTER"
                   " - consent mode {}".format(self.id))
        if to_researcher:
            template = 'email_rdbm_new_work_researcher.html'
        else:
            template = 'email_rdbm_new_work_pt_from_rdbm.html'
        html = render_email_html_to_string(template, {'letter': letter})
        email = Email.create_rdbm_email(subject, html)
        email.send()

    def process_change(self) -> None:
        """
        Called upon saving.
        Will create a letter to patient.
        May create a withdrawal-of-consent letter to researcher.
        -- Major Amendment 1 (Oct 2014) to 12/EE/0407: always withdraw consent
           and tell researchers, i.e. "active cancellation" of ongoing
           permission, where the researchers have not yet made contact.
        """
        # noinspection PyTypeChecker
        letter = Letter.create_consent_confirmation_to_patient(self)
        # ... will save
        self.notify_rdbm_of_work(letter, to_researcher=False)
        self.consider_withdrawal()
        self.current = True  # will disable current flag for others
        self.save()


# =============================================================================
# Request for patient contact
# =============================================================================

class ContactRequest(models.Model):
    CLINICIAN_INVOLVEMENT_NONE = 0
    CLINICIAN_INVOLVEMENT_REQUESTED = 1
    CLINICIAN_INVOLVEMENT_REQUIRED_YELLOW = 2
    CLINICIAN_INVOLVEMENT_REQUIRED_UNKNOWN = 3

    CLINICIAN_CONTACT_MODE_CHOICES = (
        (CLINICIAN_INVOLVEMENT_NONE,
         'No clinician involvement required or requested'),
        (CLINICIAN_INVOLVEMENT_REQUESTED,
         'Clinician involvement requested by researchers'),
        (CLINICIAN_INVOLVEMENT_REQUIRED_YELLOW,
         'Clinician involvement required by YELLOW consent mode'),
        (CLINICIAN_INVOLVEMENT_REQUIRED_UNKNOWN,
         'Clinician involvement required by UNKNOWN consent mode'),
    )

    # Created initially:
    created_at = models.DateTimeField(verbose_name="When created",
                                      auto_now_add=True)
    request_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    study = models.ForeignKey(Study)  # type: Study
    request_direct_approach = models.BooleanField(
        verbose_name="Request direct contact with patient if available"
                     " (not contact with clinician first)")
    # One of these will be non-NULL
    lookup_nhs_number = models.BigIntegerField(
        null=True,
        verbose_name="NHS number used for lookup")
    lookup_rid = models.CharField(
        max_length=MAX_HASH_LENGTH, null=True,
        verbose_name="Research ID used for lookup")
    lookup_mrid = models.CharField(
        max_length=MAX_HASH_LENGTH, null=True,
        verbose_name="Master research ID used for lookup")

    processed = models.BooleanField(default=False)
    # Below: created during processing.

    # Those numbers translate to this:
    nhs_number = models.BigIntegerField(null=True, verbose_name="NHS number")
    # ... from which:
    patient_lookup = models.ForeignKey(PatientLookup, null=True)
    consent_mode = models.ForeignKey(ConsentMode, null=True)
    # Now decisions:
    approaches_in_past_year = models.PositiveIntegerField(null=True)
    decisions = models.TextField(
        blank=True, verbose_name="Decisions made")
    decided_no_action = models.BooleanField(default=False)
    decided_send_to_researcher = models.BooleanField(default=False)
    decided_send_to_clinician = models.BooleanField(default=False)
    clinician_involvement = models.PositiveSmallIntegerField(
        choices=CLINICIAN_CONTACT_MODE_CHOICES,
        null=True)
    consent_withdrawn = models.BooleanField(default=False)
    consent_withdrawn_at = models.DateTimeField(
        verbose_name="When consent withdrawn", null=True)

    def __str__(self):
        return "[ContactRequest {}] Study {}".format(
            self.id,
            self.study_id,
        )

    @classmethod
    def create(cls,
               request: HttpRequest,
               study: Study,
               request_direct_approach: bool,
               lookup_nhs_number: int = None,
               lookup_rid: str = None,
               lookup_mrid: str = None) -> CONTACT_REQUEST_FWD_REF:
        """Create a contact request and act on it."""
        # https://docs.djangoproject.com/en/1.9/ref/request-response/
        # noinspection PyTypeChecker
        cr = cls(request_by=request.user,
                 study=study,
                 request_direct_approach=request_direct_approach,
                 lookup_nhs_number=lookup_nhs_number,
                 lookup_rid=lookup_rid,
                 lookup_mrid=lookup_mrid)
        cr.save()
        transaction.on_commit(
            lambda: process_contact_request.delay(cr.id)
        )  # Asynchronous
        return cr

    def process_request(self) -> None:
        self.decisionlist = []
        self.process_request_main()
        self.decisions = " ".join(self.decisionlist)
        self.processed = True
        self.save()

    def process_request_main(self) -> None:
        """
        =======================================================================
        Act on a contact request and store the decisions made.
        CORE DECISION-MAKING FUNCTION FOR THE CONSENT-TO-CONTACT PROCESS.
        =======================================================================
        The decisions parameter is a list that's appended to.
        """
        # Translate to an NHS number
        if self.lookup_nhs_number is not None:
            self.nhs_number = self.lookup_nhs_number
        elif self.lookup_rid is not None:
            # noinspection PyTypeChecker
            self.nhs_number = get_mpid(rid=self.lookup_rid)
        elif self.lookup_mrid is not None:
            # noinspection PyTypeChecker
            self.nhs_number = get_mpid(mrid=self.lookup_mrid)
        else:
            raise ValueError("No NHS number, RID, or MRID supplied.")
        # Look up patient details (afresh)
        self.patient_lookup = lookup_patient(self.nhs_number, save=True)
        # Establish consent mode (always do this to avoid NULL problem)
        ConsentMode.refresh_from_primary_clinical_record(
            nhs_number=self.nhs_number,
            created_by=self.request_by)
        self.consent_mode = ConsentMode.get_or_create(
            nhs_number=self.nhs_number,
            created_by=self.request_by)
        # Rest of processing
        self.calc_approaches_in_past_year()

        # ---------------------------------------------------------------------
        # Main decision process
        # ---------------------------------------------------------------------

        # Simple failures
        if not self.patient_lookup.pt_found:
            self.stop("no patient found")
            return
        if self.consent_mode.exclude_entirely:
            self.stop(
                "patient has exclude_entirely flag set; "
                " POTENTIALLY SERIOUS ERROR in that this patient shouldn't"
                " have been in the anonymised database.")
            return
        if self.patient_lookup.pt_dead:
            self.stop("patient is dead")
            return
        if self.consent_mode.consent_mode == ConsentMode.RED:
            self.stop("patient's consent mode is RED")
            return

        # Age?
        if self.patient_lookup.pt_dob is None:
            self.stop("patient DOB unknown")
            return
        if (not self.study.include_under_16s and
                self.patient_lookup.is_under_16()):
            self.stop("patient is under 16 and study not approved for that")
            return

        # Discharged/outside discharge criteria?
        if self.patient_lookup.pt_discharged:
            if not self.study.include_discharged:
                self.stop(
                    "patient is discharged and study not approved for that")
                return
            # if self.consent_mode.consent_mode not in (ConsentMode.GREEN,
            #                                           ConsentMode.YELLOW):
            #     self.stop("patient is discharged and consent mode is not "
            #               "GREEN or YELLOW")
            #     return
            days_since_discharge = self.patient_lookup.days_since_discharge()
            permitted_n_days = settings.PERMITTED_TO_CONTACT_DISCHARGED_PATIENTS_FOR_N_DAYS  # noqa
            if not self.consent_mode.consent_after_discharge:
                if days_since_discharge is None:
                    self.stop("patient is discharged; patient did not consent "
                              "to contact after discharge; unable to "
                              "determine days since discharge")
                    return
                if days_since_discharge > permitted_n_days:
                    self.stop(
                        "patient was discharged {} days ago; "
                        "permission exists only for up to {} days; "
                        "patient did not consent to contact after "
                        "discharge".format(
                            days_since_discharge,
                            permitted_n_days,
                        ))
                    return

        # Maximum number of approaches exceeded?
        if self.consent_mode.max_approaches_per_year > 0:
            if (self.approaches_in_past_year >=
                    self.consent_mode.max_approaches_per_year):
                self.stop(
                    "patient has had {} approaches in the past year and has "
                    "set a cap of {} per year".format(
                        self.approaches_in_past_year,
                        self.consent_mode.max_approaches_per_year,
                    )
                )
                return

        # ---------------------------------------------------------------------
        # OK. If we get here, we're going to try to contact someone!
        # ---------------------------------------------------------------------

        # Direct?
        self.save()  # makes self.id, needed for FKs
        if (self.consent_mode.consent_mode == ConsentMode.GREEN and
                self.request_direct_approach):
            # noinspection PyTypeChecker
            letter = Letter.create_researcher_approval(self)  # will save
            self.decided_send_to_researcher = True
            self.clinician_involvement = (
                ContactRequest.CLINICIAN_INVOLVEMENT_NONE)
            self.decide("GREEN: Researchers prefer direct approach and patient"
                        " has chosen green mode: send approval to researcher.")
            researcher_emailaddr = self.study.lead_researcher.email
            try:
                validate_email(researcher_emailaddr)
                # noinspection PyTypeChecker
                email = Email.create_researcher_approval_email(self, letter)
                emailtransmission = email.send()
                if emailtransmission.sent:
                    self.decide("Sent approval to researcher at {}".format(
                        researcher_emailaddr))
                    return
                self.decide(
                    "Failed to e-mail approval to researcher at {}.".format(
                        researcher_emailaddr))
                # noinspection PyTypeChecker
                self.decide(emailtransmission.failure_reason)
            except ValidationError:
                pass
            self.decide("Approval letter to researcher created and needs "
                        "printing")
            self.notify_rdbm_of_work(letter, to_researcher=True)
            return

        # All other routes are via clinician.

        # noinspection PyTypeChecker
        self.clinician_involvement = self.get_clinician_involvement(
            consent_mode_str=self.consent_mode.consent_mode,
            request_direct_approach=self.request_direct_approach)

        # Do we have a clinician?
        if not self.patient_lookup.clinician_found:
            self.stop("don't know clinician; can't proceed")
            return
        clinician_emailaddr = self.patient_lookup.clinician_email
        try:
            validate_email(clinician_emailaddr)
        except ValidationError:
            self.stop("clinician e-mail ({}) is invalid".format(
                clinician_emailaddr))
            return
        try:
            # noinspection PyTypeChecker
            validate_researcher_email_domain(clinician_emailaddr)
        except ValidationError:
            self.stop(
                "clinician e-mail ({}) is not in a permitted domain".format(
                    clinician_emailaddr))
            return

        # Warnings
        if (ContactRequest.objects
                .filter(nhs_number=self.nhs_number)
                .filter(study=self.study)
                .filter(decided_send_to_clinician=True)
                .filter(clinician_response__responded=False)
                .exists()):
            self.decide("WARNING: outstanding request to clinician for same "
                        "patient/study.")
        if (ContactRequest.objects
                .filter(nhs_number=self.nhs_number)
                .filter(study=self.study)
                .filter(decided_send_to_clinician=True)
                .filter(clinician_response__responded=True)
                .filter(clinician_response__response__in=[
                    ClinicianResponse.RESPONSE_B,
                    ClinicianResponse.RESPONSE_C,
                    ClinicianResponse.RESPONSE_D,
                ])
                .exists()):
            self.decide("WARNING: clinician has already rejected a request "
                        "about this patient/study.")

        # Send e-mail to clinician
        # noinspection PyTypeChecker
        email = Email.create_clinician_email(self)
        # ... will also create a ClinicianResponse
        emailtransmission = email.send()
        if not emailtransmission.sent:
            # noinspection PyTypeChecker
            self.decide(emailtransmission.failure_reason)
            self.stop("Failed to send e-mail to clinician at {}".format(
                clinician_emailaddr))
            # We don't set decided_send_to_clinician because this attempt has
            # failed, and we don't want to put anyone off trying again
            # immediately.
        self.decided_send_to_clinician = True
        self.decide(
            "Sent request to clinician at {}".format(clinician_emailaddr))

    @staticmethod
    def get_clinician_involvement(consent_mode_str: str,
                                  request_direct_approach: bool) -> int:
        # Let's be precise about why the clinician is involved.
        if not request_direct_approach:
            return ContactRequest.CLINICIAN_INVOLVEMENT_REQUESTED
        elif consent_mode_str == ConsentMode.YELLOW:
            return ContactRequest.CLINICIAN_INVOLVEMENT_REQUIRED_YELLOW
        else:
            # Only other possibility
            return ContactRequest.CLINICIAN_INVOLVEMENT_REQUIRED_UNKNOWN

    def decide(self, msg: str) -> None:
        self.decisionlist.append(msg)

    def stop(self, msg: str) -> None:
        self.decide("Stopping: " + msg)
        self.decided_no_action = True

    def calc_approaches_in_past_year(self) -> None:
        # How best to count this?
        # Not by e.g. calendar year, with a flag that gets reset to zero
        # annually, because you might have a limit of 5, and get 4 requests in
        # Dec 2020 and then another 4 in Jan 2021 just after the flag resets.
        # Instead, we count the number of requests to that patient in the past
        # year.
        one_year_ago = timezone.now() - datetime.timedelta(days=365)

        self.approaches_in_past_year = ContactRequest.objects.filter(
            Q(decided_send_to_researcher=True) |
            (Q(decided_send_to_clinician=True) &
                (Q(clinician_response__response=ClinicianResponse.RESPONSE_A) |
                 Q(clinician_response__response=ClinicianResponse.RESPONSE_R))),  # noqa
            nhs_number=self.nhs_number,
            created_at__gte=one_year_ago
        ).count()

    def withdraw_consent(self) -> Tuple[LETTER_FWD_REF, bool]:
        self.consent_withdrawn = True
        self.consent_withdrawn_at = timezone.now()
        self.save()
        # noinspection PyTypeChecker
        letter = Letter.create_researcher_withdrawal(self)  # will save
        researcher_emailaddr = self.study.lead_researcher.email
        email_succeeded = False
        try:
            validate_email(researcher_emailaddr)
            # noinspection PyTypeChecker
            email = Email.create_researcher_withdrawal_email(self, letter)
            emailtransmission = email.send()
            email_succeeded = emailtransmission.sent
        except ValidationError:
            pass
        return letter, email_succeeded

    def get_permission_date(self) -> Optional[datetime.datetime]:
        """When was the researcher given permission? Used for the letter
        withdrawing permission."""
        if self.decided_no_action:
            return None
        if self.decided_send_to_researcher:
            # Green route
            # noinspection PyTypeChecker
            return self.created_at
        if self.decided_send_to_clinician:
            # Yellow route -> patient -> said yes
            if hasattr(self, 'patient_response'):
                if self.patient_response.response == PatientResponse.YES:
                    return self.patient_response.created_at
        return None

    def notify_rdbm_of_work(self,
                            letter: LETTER_FWD_REF,
                            to_researcher: bool = False) -> None:
        subject = ("CHEERFUL WORK FROM RESEARCH DATABASE COMPUTER"
                   " - contact request {}".format(self.id))
        if to_researcher:
            template = 'email_rdbm_new_work_researcher.html'
        else:
            template = 'email_rdbm_new_work_pt_from_clinician.html'
        html = render_email_html_to_string(template, {'letter': letter})
        email = Email.create_rdbm_email(subject, html)
        email.send()

    def notify_rdbm_of_bad_progress(self) -> None:
        subject = ("INFO ONLY - clinician refused Research Database request"
                   " - contact request {}".format(self.id))
        html = render_email_html_to_string('email_rdbm_bad_progress.html', {
            'id': self.id,
            'response': self.clinician_response.response,
            'explanation': self.clinician_response.get_response_explanation(),
        })
        email = Email.create_rdbm_email(subject, html)
        email.send()

    def notify_rdbm_of_good_progress(self) -> None:
        subject = ("INFO ONLY - clinician agreed to Research Database request"
                   " - contact request {}".format(self.id))
        html = render_email_html_to_string('email_rdbm_good_progress.html', {
            'id': self.id,
            'response': self.clinician_response.response,
            'explanation': self.clinician_response.get_response_explanation(),
        })
        email = Email.create_rdbm_email(subject, html)
        email.send()

    def get_clinician_email_html(self, save: bool = True) -> str:
        """
        REC DOCUMENTS 09, 11, 13 (A): E-mail to clinician
        E-mail to clinician asking them to pass on contact request.

        URL method (path, querystring, both?): see notes in core/utils.py

        In this case, decision: since we are creating a ClinicianResponse, we
        should use its ModelForm.
            - URL path for PK
            - querystring for other parameters, with form-based validation
        """
        clinician_response = ClinicianResponse.create(self, save=save)
        if not save:
            clinician_response.id = -1  # dummy PK, guaranteed to fail
        context = {
            'contact_request': self,
            'study': self.study,
            'patient_lookup': self.patient_lookup,
            'consent_mode': self.consent_mode,
            'settings': settings,
            'url_yes': clinician_response.get_abs_url_yes(),
            'url_no': clinician_response.get_abs_url_no(),
            'url_maybe': clinician_response.get_abs_url_maybe(),
            'permitted_to_contact_discharged_patients_for_n_days':
                settings.PERMITTED_TO_CONTACT_DISCHARGED_PATIENTS_FOR_N_DAYS,
            'permitted_to_contact_discharged_patients_for_n_years':
                days_to_years(
                    settings.PERMITTED_TO_CONTACT_DISCHARGED_PATIENTS_FOR_N_DAYS),  # noqa
        }
        return render_email_html_to_string('email_clinician.html', context)

    def get_approval_letter_html(self) -> str:
        """
        REC DOCUMENT 15.
        Letter to researcher approving contact.
        """
        context = {
            # Letter bits
            'address_from': (
                settings.RDBM_ADDRESS +
                [settings.RDBM_TELEPHONE, settings.RDBM_EMAIL]
            ),
            'address_to': self.study.get_lead_researcher_name_address(),
            'salutation': self.study.get_lead_researcher_salutation(),
            'signatory_name': settings.RDBM_NAME,
            'signatory_title': settings.RDBM_TITLE,
            # Specific bits
            'contact_request': self,
            'study': self.study,
            'patient_lookup': self.patient_lookup,
            'consent_mode': self.consent_mode,

            'permitted_to_contact_discharged_patients_for_n_days':
                settings.PERMITTED_TO_CONTACT_DISCHARGED_PATIENTS_FOR_N_DAYS,
            'permitted_to_contact_discharged_patients_for_n_years':
                days_to_years(
                    settings.PERMITTED_TO_CONTACT_DISCHARGED_PATIENTS_FOR_N_DAYS),  # noqa

            'RDBM_ADDRESS': settings.RDBM_ADDRESS,
        }
        return render_pdf_html_to_string('letter_researcher_approve.html',
                                         context, patient=False)

    def get_withdrawal_letter_html(self) -> str:
        """
        REC DOCUMENT 16.
        Letter to researcher notifying them of withdrawal of consent.
        """
        context = {
            # Letter bits
            'address_from': (
                settings.RDBM_ADDRESS +
                [settings.RDBM_TELEPHONE, settings.RDBM_EMAIL]
            ),
            'address_to': self.study.get_lead_researcher_name_address(),
            'salutation': self.study.get_lead_researcher_salutation(),
            'signatory_name': settings.RDBM_NAME,
            'signatory_title': settings.RDBM_TITLE,
            # Specific bits
            'contact_request': self,
            'study': self.study,
            'patient_lookup': self.patient_lookup,
            'consent_mode': self.consent_mode,
        }
        return render_pdf_html_to_string('letter_researcher_withdraw.html',
                                         context, patient=False)

    def get_approval_email_html(self) -> str:
        """Simple e-mail to researcher attaching letter."""
        context = {
            'contact_request': self,
            'study': self.study,
            'patient_lookup': self.patient_lookup,
            'consent_mode': self.consent_mode,
        }
        return render_email_html_to_string('email_researcher_approval.html',
                                           context)

    def get_withdrawal_email_html(self) -> str:
        """Simple e-mail to researcher attaching letter."""
        context = {
            'contact_request': self,
            'study': self.study,
            'patient_lookup': self.patient_lookup,
            'consent_mode': self.consent_mode,
        }
        return render_email_html_to_string('email_researcher_withdrawal.html',
                                           context)

    def get_letter_clinician_to_pt_re_study(self) -> str:
        """
        REC DOCUMENTS 10, 12, 14: draft letters from clinician to patient, with
        decision form.
        """
        patient_lookup = self.patient_lookup
        if not patient_lookup:
            raise Http404("No patient_lookup: is the back-end message queue "
                          "(e.g. Celery + RabbitMQ) running?")
        yellow = (self.clinician_involvement ==
                  ContactRequest.CLINICIAN_INVOLVEMENT_REQUIRED_YELLOW)
        context = {
            # Letter bits
            'address_from': patient_lookup.clinician_address_components(),
            'address_to': patient_lookup.pt_name_address_components(),
            'salutation': patient_lookup.pt_salutation(),
            'signatory_name':
            patient_lookup.clinician_title_forename_surname(),
            'signatory_title': patient_lookup.clinician_signatory_title,
            # Specific bits
            'contact_request': self,
            'study': self.study,
            'patient_lookup': patient_lookup,
            'settings': settings,

            'extra_form': self.is_extra_form(),
            'yellow': yellow,
            'unknown_consent_mode': self.is_consent_mode_unknown(),
        }
        return render_pdf_html_to_string(
            'letter_patient_from_clinician_re_study.html',
            context, patient=True)

    def is_extra_form(self) -> bool:
        study = self.study
        clinician_requested = not self.request_direct_approach
        extra_form = (clinician_requested and
                      study.subject_form_template_pdf.name)
        # log.debug("clinician_requested: {}".format(clinician_requested))
        # log.debug("extra_form: {}".format(extra_form))
        return extra_form

    def is_consent_mode_unknown(self) -> bool:
        return not self.consent_mode.consent_mode

    def get_decision_form_to_pt_re_study(self) -> str:
        n_forms = 1
        extra_form = self.is_extra_form()
        if extra_form:
            n_forms += 1
        yellow = (self.clinician_involvement ==
                  ContactRequest.CLINICIAN_INVOLVEMENT_REQUIRED_YELLOW)
        unknown = (self.clinician_involvement ==
                   ContactRequest.CLINICIAN_INVOLVEMENT_REQUIRED_UNKNOWN)
        if unknown:
            n_forms += 1
        context = {
            'contact_request': self,
            'study': self.study,
            'patient_lookup': self.patient_lookup,
            'settings': settings,

            'extra_form': extra_form,
            'n_forms': n_forms,
            'yellow': yellow,
        }
        return render_pdf_html_to_string(
            'decision_form_to_patient_re_study.html', context, patient=True)

    def get_clinician_pack_pdf(self) -> bytes:
        # Order should match letter...

        # Letter to patient from clinician
        pdf_plans = [PdfPlan(
            is_html=True,
            html=self.get_letter_clinician_to_pt_re_study()
        )]
        # Study details
        if self.study.study_details_pdf:
            pdf_plans.append(PdfPlan(
                is_filename=True,
                filename=self.study.study_details_pdf.path
            ))
        # Decision form about this study
        pdf_plans.append(PdfPlan(
            is_html=True,
            html=self.get_decision_form_to_pt_re_study()
        ))
        # Additional form for this study
        if self.is_extra_form():
            if self.study.subject_form_template_pdf:
                pdf_plans.append(PdfPlan(
                    is_filename=True,
                    filename=self.study.subject_form_template_pdf.path
                ))
        # Traffic-light decision form, if consent mode unknown
        if self.is_consent_mode_unknown():
            # 2017-03-03: changed to a personalized version

            # try:
            #     leaflet = Leaflet.objects.get(
            #         name=Leaflet.CPFT_TRAFFICLIGHT_CHOICE)
            #     pdf_plans.append(PdfPlan(is_filename=True,
            #                              filename=leaflet.pdf.path))
            # except ObjectDoesNotExist:
            #     log.warning("Missing traffic-light leaflet!")
            #     email_rdbm_task.delay(
            #         subject="ERROR FROM RESEARCH DATABASE COMPUTER",
            #         text=(
            #             "Missing traffic-light leaflet! Incomplete clinician "
            #             "pack accessed for contact request {}.".format(
            #                 self.id)
            #         )
            #     )

            pdf_plans.append(PdfPlan(
                is_html=True,
                html=self.patient_lookup.get_traffic_light_decision_form()
            ))
        # General info leaflet
        try:
            leaflet = Leaflet.objects.get(name=Leaflet.CPFT_TPIR)
            pdf_plans.append(PdfPlan(is_filename=True,
                                     filename=leaflet.pdf.path))
        except ObjectDoesNotExist:
            log.warning("Missing taking-part-in-research leaflet!")
            email_rdbm_task.delay(
                subject="ERROR FROM RESEARCH DATABASE COMPUTER",
                text=(
                    "Missing taking-part-in-research leaflet! Incomplete "
                    "clinician pack accessed for contact request {}.".format(
                        self.id)
                )
            )
        return get_concatenated_pdf_in_memory(pdf_plans, start_recto=True)

    def get_mgr_admin_url(self) -> str:
        from crate_anon.crateweb.core.admin import mgr_admin_site  # delayed import  # noqa
        return admin_view_url(mgr_admin_site, self)


# =============================================================================
# Clinician response
# =============================================================================

class ClinicianResponse(models.Model):
    TOKEN_LENGTH_CHARS = 20
    # info_bits = math.log(math.pow(26 + 26 + 10, TOKEN_LENGTH_CHARS), 2)
    # p_guess = math.pow(0.5, info_bits)

    RESPONSE_A = 'A'
    RESPONSE_B = 'B'
    RESPONSE_C = 'C'
    RESPONSE_D = 'D'
    RESPONSE_R = 'R'
    RESPONSES = (
        (RESPONSE_R, 'R: Clinician asks RDBM to pass request to patient'),
        (RESPONSE_A, 'A: Clinician will pass the request to the patient'),
        (RESPONSE_B, 'B: Clinician vetoes on clinical grounds'),
        (RESPONSE_C, 'C: Patient is definitely ineligible'),
        (RESPONSE_D, 'D: Patient is dead/discharged or details are defunct'),
    )

    ROUTE_EMAIL = 'e'
    ROUTE_WEB = 'w'
    RESPONSE_ROUTES = (
        (ROUTE_EMAIL, 'E-mail'),
        (ROUTE_WEB, 'Web'),
    )

    EMAIL_CHOICE_Y = 'y'
    EMAIL_CHOICE_N = 'n'
    EMAIL_CHOICE_TELL_ME_MORE = 'more'
    EMAIL_CHOICES = (
        (EMAIL_CHOICE_Y, 'Yes'),
        (EMAIL_CHOICE_N, 'No'),
        (EMAIL_CHOICE_TELL_ME_MORE, 'Tell me more'),
    )

    created_at = models.DateTimeField(verbose_name="When created",
                                      auto_now_add=True)
    contact_request = models.OneToOneField(ContactRequest,
                                           related_name="clinician_response")
    token = models.CharField(max_length=TOKEN_LENGTH_CHARS)
    responded = models.BooleanField(default=False, verbose_name="Responded?")
    responded_at = models.DateTimeField(verbose_name="When responded",
                                        null=True)
    response_route = models.CharField(max_length=1, choices=RESPONSE_ROUTES)
    email_choice = models.CharField(max_length=4, choices=EMAIL_CHOICES)
    response = models.CharField(max_length=1, choices=RESPONSES)
    veto_reason = models.TextField(
        blank=True,
        verbose_name="Reason for clinical veto")
    ineligible_reason = models.TextField(
        blank=True,
        verbose_name="Reason patient is ineligible")
    pt_uncontactable_reason = models.TextField(
        blank=True,
        verbose_name="Reason patient is not contactable")
    clinician_confirm_name = models.CharField(
        max_length=255, verbose_name="Type your name to confirm")
    charity_amount_due = models.DecimalField(max_digits=8, decimal_places=2,
                                             default=0)
    # ... set to settings.CHARITY_AMOUNT_CLINICIAN_RESPONSE upon response

    def get_response_explanation(self) -> str:
        # log.debug("get_response_explanation: {}".format(self.response))
        # noinspection PyTypeChecker
        return choice_explanation(self.response, ClinicianResponse.RESPONSES)

    @classmethod
    def create(cls,
               contact_request: ContactRequest,
               save: bool = True) -> CLINICIAN_RESPONSE_FWD_REF:
        newtoken = get_random_string(ClinicianResponse.TOKEN_LENGTH_CHARS)
        # https://github.com/django/django/blob/master/django/utils/crypto.py#L51  # noqa
        clinician_response = cls(
            contact_request=contact_request,
            token=newtoken,
        )
        if save:
            clinician_response.save()
        return clinician_response

    def get_abs_url_path(self) -> str:
        rev = reverse('clinician_response', args=[self.id])
        url = site_absolute_url(rev)
        return url

    def get_common_querydict(self, email_choice: str) -> QueryDict:
        querydict = QueryDict(mutable=True)
        querydict['token'] = self.token
        querydict['email_choice'] = email_choice
        return querydict

    def get_abs_url(self, email_choice: str) -> str:
        path = self.get_abs_url_path()
        querydict = self.get_common_querydict(email_choice)
        return url_with_querystring(path, querydict)

    def get_abs_url_yes(self) -> str:
        return self.get_abs_url(ClinicianResponse.EMAIL_CHOICE_Y)

    def get_abs_url_no(self) -> str:
        return self.get_abs_url(ClinicianResponse.EMAIL_CHOICE_N)

    def get_abs_url_maybe(self) -> str:
        return self.get_abs_url(ClinicianResponse.EMAIL_CHOICE_TELL_ME_MORE)

    def __str__(self):
        return "[ClinicianResponse {}] ContactRequest {}".format(
            self.id,
            self.contact_request_id,
        )

    def finalize_a(self) -> None:
        """
        Call this when the clinician completes their response.
        Part A: immediate, for acknowledgement.
        """
        self.responded = True
        self.responded_at = timezone.now()
        self.charity_amount_due = settings.CHARITY_AMOUNT_CLINICIAN_RESPONSE
        self.save()

    def finalize_b(self) -> None:
        """
        Call this when the clinician completes their response.
        Part B: background.
        """
        if self.response == ClinicianResponse.RESPONSE_R:
            # noinspection PyTypeChecker
            letter = Letter.create_request_to_patient(
                self.contact_request, rdbm_may_view=True)
            # ... will save
            # noinspection PyTypeChecker
            PatientResponse.create(self.contact_request)
            # ... will save
            self.contact_request.notify_rdbm_of_work(letter)
        elif self.response == ClinicianResponse.RESPONSE_A:
            # noinspection PyTypeChecker
            Letter.create_request_to_patient(
                self.contact_request, rdbm_may_view=False)
            # ... return value not used
            # noinspection PyTypeChecker
            PatientResponse.create(self.contact_request)
            self.contact_request.notify_rdbm_of_good_progress()
        elif self.response in (ClinicianResponse.RESPONSE_B,
                               ClinicianResponse.RESPONSE_C,
                               ClinicianResponse.RESPONSE_D):
            self.contact_request.notify_rdbm_of_bad_progress()
        self.save()


# =============================================================================
# Patient response
# =============================================================================

PATIENT_RESPONSE_FWD_REF = "PatientResponse"


class PatientResponse(Decision):
    YES = 1
    NO = 2
    RESPONSES = (
        (YES, '1: Yes'),
        (NO, '2: No'),
    )
    created_at = models.DateTimeField(verbose_name="When created",
                                      auto_now_add=True)
    contact_request = models.OneToOneField(ContactRequest,
                                           related_name="patient_response")
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    response = models.PositiveSmallIntegerField(
        null=True,
        choices=RESPONSES, verbose_name="Patient's response")

    def __str__(self):
        if self.response:
            # noinspection PyTypeChecker
            suffix = "response was {}".format(choice_explanation(
                self.response, PatientResponse.RESPONSES))
        else:
            suffix = "AWAITING RESPONSE"
        return "Patient response {} (contact request {}, study {}): {}".format(
            self.id,
            self.contact_request.id,
            self.contact_request.study.id,
            suffix,
        )

    @classmethod
    def create(cls, contact_request: ContactRequest) \
            -> PATIENT_RESPONSE_FWD_REF:
        patient_response = cls(contact_request=contact_request)
        patient_response.save()
        return patient_response

    def process_response(self) -> None:
        # log.debug("process_response: PatientResponse: {}".format(
        #     modelrepr(self)))
        if self.response == PatientResponse.YES:
            contact_request = self.contact_request
            # noinspection PyTypeChecker
            letter = Letter.create_researcher_approval(contact_request)
            # ... will save
            # noinspection PyTypeChecker
            email = Email.create_researcher_approval_email(contact_request,
                                                           letter)
            emailtransmission = email.send()
            emailed = emailtransmission.sent
            if not emailed:
                contact_request.notify_rdbm_of_work(letter, to_researcher=True)


# =============================================================================
# Letter, and record of letter being printed
# =============================================================================

class Letter(models.Model):
    created_at = models.DateTimeField(verbose_name="When created",
                                      auto_now_add=True)
    pdf = models.FileField(storage=privatestorage)
    # Other flags:
    to_clinician = models.BooleanField(default=False)
    to_researcher = models.BooleanField(default=False)
    to_patient = models.BooleanField(default=False)
    rdbm_may_view = models.BooleanField(default=False)
    study = models.ForeignKey(Study, null=True)
    contact_request = models.ForeignKey(ContactRequest, null=True)
    sent_manually_at = models.DateTimeField(null=True)

    def __str__(self):
        return "Letter {}".format(self.id)

    @classmethod
    def create(cls,
               basefilename: str,
               html: str = None,
               pdf: bytes = None,
               to_clinician: bool = False,
               to_researcher: bool = False,
               to_patient: bool = False,
               rdbm_may_view: bool = False,
               study: Study = None,
               contact_request: ContactRequest = None,
               debug_store_html: bool = False) -> LETTER_FWD_REF:
        # Writing to a FileField directly: you can use field.save(), but then
        # you having to write one file and copy to another, etc.
        # Here we use the method of assigning to field.name (you can't assign
        # to field.path). Also, note that you should never read
        # the path attribute if name is blank; it raises an exception.
        if (html and pdf) or (not html and not pdf):
            raise ValueError("Invalid html/pdf options to Letter.create")
        filename_in_storage = os.path.join("letter", basefilename)
        abs_filename = os.path.join(settings.PRIVATE_FILE_STORAGE_ROOT,
                                    filename_in_storage)
        os.makedirs(os.path.dirname(abs_filename), exist_ok=True)
        if html:
            # HTML supplied
            if debug_store_html:
                with open(abs_filename + ".html", 'w') as f:
                    f.write(html)
            pdf_from_html(html,
                          header_html=None,
                          footer_html=None,
                          output_path=abs_filename)
        else:
            # PDF supplied in memory
            with open(abs_filename, 'wb') as f:
                f.write(pdf)
        letter = cls(to_clinician=to_clinician,
                     to_researcher=to_researcher,
                     to_patient=to_patient,
                     rdbm_may_view=rdbm_may_view,
                     study=study,
                     contact_request=contact_request)
        letter.pdf.name = filename_in_storage
        letter.save()
        return letter

    @classmethod
    def create_researcher_approval(cls, contact_request: ContactRequest) \
            -> LETTER_FWD_REF:
        basefilename = "cr{}_res_approve_{}.pdf".format(
            contact_request.id,
            string_time_now(),
        )
        html = contact_request.get_approval_letter_html()
        # noinspection PyTypeChecker
        return cls.create(basefilename,
                          html=html,
                          to_researcher=True,
                          study=contact_request.study,
                          contact_request=contact_request,
                          rdbm_may_view=True)

    @classmethod
    def create_researcher_withdrawal(cls, contact_request: ContactRequest) \
            -> LETTER_FWD_REF:
        basefilename = "cr{}_res_withdraw_{}.pdf".format(
            contact_request.id,
            string_time_now(),
        )
        html = contact_request.get_withdrawal_letter_html()
        # noinspection PyTypeChecker
        return cls.create(basefilename,
                          html=html,
                          to_researcher=True,
                          study=contact_request.study,
                          contact_request=contact_request,
                          rdbm_may_view=True)

    @classmethod
    def create_request_to_patient(cls,
                                  contact_request: ContactRequest,
                                  rdbm_may_view: bool = False) \
            -> LETTER_FWD_REF:
        basefilename = "cr{}_to_pt_{}.pdf".format(
            contact_request.id,
            string_time_now(),
        )
        pdf = contact_request.get_clinician_pack_pdf()
        # noinspection PyTypeChecker
        letter = cls.create(basefilename,
                            pdf=pdf,
                            to_patient=True,
                            study=contact_request.study,
                            contact_request=contact_request,
                            rdbm_may_view=rdbm_may_view)
        if not rdbm_may_view:
            # Letter is from clinician directly; clinician will print
            letter.mark_sent()
        return letter

    @classmethod
    def create_consent_confirmation_to_patient(
            cls, consent_mode: ConsentMode) -> LETTER_FWD_REF:
        basefilename = "cm{}_to_pt_{}.pdf".format(
            consent_mode.id,
            string_time_now(),
        )
        html = consent_mode.get_confirm_traffic_to_patient_letter_html()
        return cls.create(basefilename,
                          html=html,
                          to_patient=True,
                          rdbm_may_view=True)

    def mark_sent(self):
        self.sent_manually_at = timezone.now()
        self.save()


# noinspection PyUnusedLocal
@receiver(models.signals.post_delete, sender=Letter)
def auto_delete_letter_files_on_delete(sender: Type[Letter],
                                       instance: Letter,
                                       **kwargs: Any) -> None:
    """Deletes files from filesystem when Letter object is deleted."""
    auto_delete_files_on_instance_delete(instance, ['pdf'])


# noinspection PyUnusedLocal
@receiver(models.signals.pre_save, sender=Letter)
def auto_delete_letter_files_on_change(sender: Type[Letter],
                                       instance: Letter,
                                       **kwargs: Any) -> None:
    """Deletes files from filesystem when Letter object is changed."""
    auto_delete_files_on_instance_change(instance, ['pdf'], Letter)


# =============================================================================
# Record of sent e-mails
# =============================================================================

class Email(models.Model):
    # Let's not record host/port/user. It's configured into the settings.
    created_at = models.DateTimeField(verbose_name="When created",
                                      auto_now_add=True)
    sender = models.CharField(max_length=255, default=settings.EMAIL_SENDER)
    recipient = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    msg_text = models.TextField()
    msg_html = models.TextField()
    # Other flags and links:
    to_clinician = models.BooleanField(default=False)
    to_researcher = models.BooleanField(default=False)
    to_patient = models.BooleanField(default=False)
    study = models.ForeignKey(Study, null=True)
    contact_request = models.ForeignKey(ContactRequest, null=True)
    letter = models.ForeignKey(Letter, null=True)
    # Transmission attempts are in EmailTransmission.
    # Except that filtering in the admin

    def __str__(self):
        return "Email {} to {}".format(self.id, self.recipient)

    @classmethod
    def create_clinician_email(cls, contact_request: ContactRequest) \
            -> EMAIL_FWD_REF:
        recipient = contact_request.patient_lookup.clinician_email
        subject = (
            "RESEARCH REQUEST on behalf of {researcher}, contact request "
            "code {contact_req_code}".format(
                researcher=contact_request.study.lead_researcher.
                profile.get_title_forename_surname(),
                contact_req_code=contact_request.id
            )
        )
        html = contact_request.get_clinician_email_html()
        email = cls(recipient=recipient,
                    subject=subject,
                    msg_html=html,
                    study=contact_request.study,
                    contact_request=contact_request,
                    to_clinician=True)
        email.save()
        return email

    @classmethod
    def create_researcher_approval_email(
            cls,
            contact_request: ContactRequest,
            letter: Letter) -> EMAIL_FWD_REF:
        recipient = contact_request.study.lead_researcher.email
        subject = (
            "APPROVAL TO CONTACT PATIENT: contact request "
            "code {contact_req_code}".format(
                contact_req_code=contact_request.id
            )
        )
        html = contact_request.get_approval_email_html()
        email = cls(recipient=recipient,
                    subject=subject,
                    msg_html=html,
                    study=contact_request.study,
                    contact_request=contact_request,
                    letter=letter,
                    to_researcher=True)
        email.save()
        EmailAttachment.create(email=email,
                               fileobj=letter.pdf,
                               content_type=CONTENTTYPE_PDF)  # will save
        return email

    @classmethod
    def create_researcher_withdrawal_email(
            cls,
            contact_request: ContactRequest,
            letter: Letter) -> EMAIL_FWD_REF:
        recipient = contact_request.study.lead_researcher.email
        subject = (
            "WITHDRAWAL OF APPROVAL TO CONTACT PATIENT: contact request "
            "code {contact_req_code}".format(
                contact_req_code=contact_request.id
            )
        )
        html = contact_request.get_withdrawal_email_html()
        email = cls(recipient=recipient,
                    subject=subject,
                    msg_html=html,
                    study=contact_request.study,
                    contact_request=contact_request,
                    letter=letter,
                    to_researcher=True)
        email.save()
        EmailAttachment.create(email=email,
                               fileobj=letter.pdf,
                               content_type=CONTENTTYPE_PDF)  # will save
        return email

    @classmethod
    def create_rdbm_email(cls, subject: str, html: str) -> EMAIL_FWD_REF:
        email = cls(recipient=settings.RDBM_EMAIL,
                    subject=subject,
                    msg_html=html)
        email.save()
        return email

    @classmethod
    def create_rdbm_text_email(cls, subject: str, text: str) -> EMAIL_FWD_REF:
        email = cls(recipient=settings.RDBM_EMAIL,
                    subject=subject,
                    msg_text=text)
        email.save()
        return email

    def has_been_sent(self) -> bool:
        return self.emailtransmission_set.filter(sent=True).exists()

    def send(self,
             user: settings.AUTH_USER_MODEL = None,
             resend: bool = False) -> Optional[EMAIL_TRANSMISSION_FWD_REF]:
        if self.has_been_sent() and not resend:
            log.error("Trying to send e-mail twice: ID={}".format(self.id))
            return None
        if settings.SAFETY_CATCH_ON:
            self.recipient = settings.DEVELOPER_EMAIL
        try:
            if self.msg_html and not self.msg_text:
                # HTML-only email
                # http://www.masnun.com/2014/01/09/django-sending-html-only-email.html  # noqa
                msg = EmailMessage(subject=self.subject,
                                   body=self.msg_html,
                                   from_email=self.sender,
                                   to=[self.recipient])
                msg.content_subtype = "html"  # Main content is now text/html
            else:
                # Text only, or separate text/HTML
                msg = EmailMultiAlternatives(subject=self.subject,
                                             body=self.msg_text,
                                             from_email=self.sender,
                                             to=[self.recipient])
                if self.msg_html:
                    msg.attach_alternative(self.msg_html, "text/html")
            for attachment in self.emailattachment_set.all():
                # don't use msg.attach_file() if you want to control
                # the outbound filename; use msg.attach()
                if not attachment.file:
                    continue
                path = attachment.file.path
                if not attachment.sent_filename:
                    attachment.sent_filename = os.path.basename(path)
                    attachment.save()
                with open(path, 'rb') as f:
                    content = f.read()
                msg.attach(attachment.sent_filename,
                           content,
                           attachment.content_type or None)
            msg.send()
            sent = True
            failure_reason = ''
        except Exception as e:
            sent = False
            failure_reason = str(e)
        self.save()
        emailtransmission = EmailTransmission(email=self, by=user, sent=sent,
                                              failure_reason=failure_reason)
        emailtransmission.save()
        return emailtransmission

    def resend(self, user: settings.AUTH_USER_MODEL) -> None:
        return self.send(user=user, resend=True)


EMAIL_ATTACHMENT_FWD_REF = "EmailAttachment"


class EmailAttachment(models.Model):
    """E-mail attachment class that does NOT manage its own files, i.e. if
    the attachment object is deleted, the files won't be. Use this for
    referencing files already stored elsewhere in the database."""
    email = models.ForeignKey(Email)
    file = models.FileField(storage=privatestorage)
    sent_filename = models.CharField(null=True, max_length=255)
    content_type = models.CharField(null=True, max_length=255)
    owns_file = models.BooleanField(default=False)

    def exists(self) -> bool:
        if not self.file:
            return False
        return os.path.isfile(self.file.path)

    def size(self) -> int:
        if not self.file:
            return 0
        return os.path.getsize(self.file.path)

    @classmethod
    def create(cls,
               email: Email,
               fileobj: models.FileField,
               content_type: str,
               sent_filename: str = None,
               owns_file=False) -> EMAIL_ATTACHMENT_FWD_REF:
        if sent_filename is None:
            sent_filename = os.path.basename(fileobj.name)
        attachment = cls(email=email,
                         file=fileobj,
                         sent_filename=sent_filename,
                         content_type=content_type,
                         owns_file=owns_file)
        attachment.save()
        return attachment


# noinspection PyUnusedLocal
@receiver(models.signals.post_delete, sender=EmailAttachment)
def auto_delete_emailattachment_files_on_delete(sender: Type[EmailAttachment],
                                                instance: EmailAttachment,
                                                **kwargs: Any) -> None:
    """Deletes files from filesystem when EmailAttachment object is deleted."""
    if instance.owns_file:
        auto_delete_files_on_instance_delete(instance, ['file'])


# noinspection PyUnusedLocal
@receiver(models.signals.pre_save, sender=EmailAttachment)
def auto_delete_emailattachment_files_on_change(sender: Type[EmailAttachment],
                                                instance: EmailAttachment,
                                                **kwargs: Any) -> None:
    """Deletes files from filesystem when EmailAttachment object is changed."""
    if instance.owns_file:
        auto_delete_files_on_instance_change(instance, ['file'],
                                             EmailAttachment)


class EmailTransmission(models.Model):
    email = models.ForeignKey(Email)
    at = models.DateTimeField(verbose_name="When sent", auto_now_add=True)
    by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                           related_name="emailtransmissions")
    sent = models.BooleanField(default=False)
    failure_reason = models.TextField(verbose_name="Reason sending failed")

    def __str__(self):
        return "Email transmission at {} by {}: {}".format(
            self.at,
            self.by or "(system)",
            "success" if self.sent
            else "failure: {}".format(self.failure_reason)
        )


# =============================================================================
# A dummy set of objects, for template testing.
# Linked, so cross-references work.
# Don't save() them!
# =============================================================================

class DummyObjectCollection(object):
    def __init__(self,
                 contact_request: ContactRequest,
                 consent_mode: ConsentMode,
                 patient_lookup: PatientLookup,
                 study: Study):
        self.contact_request = contact_request
        self.consent_mode = consent_mode
        self.patient_lookup = patient_lookup
        self.study = study


def make_dummy_objects(request: HttpRequest) -> DummyObjectCollection:
    """
    We want to create these objects in memory, without saving to the DB.
    However, Django  is less good at SQLAlchemy for this, and saves.

    - http://stackoverflow.com/questions/7908349/django-making-relationships-in-memory-without-saving-to-db  # noqa
    - https://code.djangoproject.com/ticket/17253
    - http://stackoverflow.com/questions/23372786/django-models-assigning-foreignkey-object-without-saving-to-database  # noqa
    - http://stackoverflow.com/questions/7121341/django-adding-objects-to-a-related-set-without-saving-to-db  # noqa

    A simple method works for an SQLite backend database but fails with
    an IntegrityError for MySQL/SQL Server. For example:

        IntegrityError at /draft_traffic_light_decision_form/-1/html/
        (1452, 'Cannot add or update a child row: a foreign key constraint
        fails (`crate_django`.`consent_study_researchers`, CONSTRAINT
        `consent_study_researchers_study_id_19bb255f_fk_consent_study_id`
        FOREIGN KEY (`study_id`) REFERENCES `consent_study` (`id`))')

    This occurs in the first creation, of a Study, and only if you specify
    'researchers'.

    The reason for the crash is that 'researchers' is a ManyToManyField, and
    Django is trying to set the user.studies_as_researcher back-reference, but
    can't do so because the Study doesn't have a PK yet.

    Since this is a minor thing, and templates are unaffected, and this is only
    for debugging, let's ignore it.
    """
    def get_int(query_param_name: str, default: Optional[int]) -> int:
        try:
            return int(request.GET.get(query_param_name, default))
        except (TypeError, ValueError):
            return default

    def get_str(query_param_name: str, default: Optional[str]) -> str:
        return request.GET.get(query_param_name, default)

    age = get_int('age', 40)
    age_months = get_int('age_months', 2)
    today = datetime.date.today()
    dob = today - relativedelta(years=age, months=age_months)

    consent_mode_str = get_str('consent_mode', None)
    if consent_mode_str not in (None, ConsentMode.RED, ConsentMode.YELLOW,
                                ConsentMode.GREEN):
        consent_mode_str = None

    request_direct_approach = bool(get_int('request_direct_approach', 1))
    clinician_involvement = ContactRequest.get_clinician_involvement(
        consent_mode_str=consent_mode_str,
        request_direct_approach=request_direct_approach)

    consent_after_discharge = bool(get_int('consent_after_discharge', 0))

    nhs_number = 1234567890
    study = Study(
        id=TEST_ID,
        institutional_id=9999999999999,
        title="Investigation of the psychokinetic ability of mussels",
        lead_researcher=request.user,
        # researchers=[request.user],  # THIS BREAKS IT.
        # ... actual crash is in
        #   django/db/models/fields/related_descriptors.py:500, in
        #   ReverseManyToOneDescriptor.__set__(), calling
        #   manager.set(value)
        registered_at=datetime.datetime.now(),
        summary="Double-blind comparison of filter feeders’ ability to "
                "move water unobstructed versus through a rigid barrier",
        search_methods_planned="Generalized trawl",
        patient_contact=True,
        include_under_16s=True,
        include_lack_capacity=True,
        clinical_trial=True,
        request_direct_approach=clinician_involvement,
        approved_by_rec=True,
        rec_reference="blah/999",
        approved_locally=True,
        local_approval_at=True,
        study_details_pdf=None,
        subject_form_template_pdf=None,
    )
    # import pdb; pdb.set_trace()
    consent_mode = ConsentMode(
        id=TEST_ID,
        nhs_number=nhs_number,
        current=True,
        created_by=request.user,
        exclude_entirely=False,
        consent_mode=consent_mode_str,
        consent_after_discharge=consent_after_discharge,
        max_approaches_per_year=0,
        other_requests="",
        prefers_email=False,
        changed_by_clinician_override=False,
        source="Fictional",
    )
    patient_lookup = PatientLookup(
        id=TEST_ID,
        # PatientLookupBase
        pt_local_id_description="MyEMR#",
        pt_local_id_number=987654,
        pt_dob=dob,
        pt_dod=None,
        pt_dead=False,
        pt_discharged=False,
        pt_discharge_date=None,
        pt_sex=PatientLookupBase.MALE,
        pt_title="Mr",
        pt_first_name="John",
        pt_last_name="Smith",
        pt_address_1="The Farthings",
        pt_address_2="1 Penny Lane",
        pt_address_3="Mordenville",
        pt_address_4="Slowtown",
        pt_address_5="Pembrokeshire",
        pt_address_6="CB1 0ZZ",
        pt_address_7="UK",
        pt_telephone="01223 000000",
        pt_email="john@smith.com",
        gp_title="Dr",
        gp_first_name="Gordon",
        gp_last_name="Generalist",
        gp_address_1="Honeysuckle Medical Practice",
        gp_address_2="99 Bloom Street",
        gp_address_3="Mordenville",
        gp_address_4="Slowtown",
        gp_address_5="Pembrokeshire",
        gp_address_6="CB1 9QQ",
        gp_address_7="UK",
        gp_telephone="01223 111111",
        gp_email="g.generalist@honeysuckle.nhs.uk",
        clinician_title="Dr",
        clinician_first_name="Petra",
        clinician_last_name="Psychiatrist",
        clinician_address_1="Union House",
        clinician_address_2="37 Union Lane",
        clinician_address_3="Chesterton",
        clinician_address_4="Cambridge",
        clinician_address_5="Cambridgeshire",
        clinician_address_6="CB4 1PR",
        clinician_address_7="UK",
        clinician_telephone="01223 222222",
        clinician_email="p.psychiatrist@cpft_or_similar.nhs.uk",
        clinician_is_consultant=True,
        clinician_signatory_title="Consultant psychiatrist",
        # PatientLookup
        nhs_number=nhs_number,
        source_db="Fictional database",
        decisions="No real decisions",
        secret_decisions="No real secret decisions",
        pt_found=True,
        gp_found=True,
        clinician_found=True,
    )
    contact_request = ContactRequest(
        id=TEST_ID,
        request_by=request.user,
        study=study,
        lookup_rid=9999999,
        processed=True,
        nhs_number=nhs_number,
        patient_lookup=patient_lookup,
        consent_mode=consent_mode,
        approaches_in_past_year=0,
        decisions="No decisions required",
        decided_no_action=False,
        decided_send_to_researcher=False,
        decided_send_to_clinician=True,
        clinician_involvement=clinician_involvement,
        consent_withdrawn=False,
        consent_withdrawn_at=None,

    )

    return DummyObjectCollection(
        contact_request=contact_request,
        consent_mode=consent_mode,
        patient_lookup=patient_lookup,
        study=study,
    )


# =============================================================================
# Testing an ISO-based millisecond-precision date/time field with timezone
# =============================================================================

# class BlibbleTest(models.Model):
#     at = IsoDateTimeTzField()
#
#     class Meta:
#         managed = True
#         db_table = 'consent_test'
#         verbose_name_plural = "no ideas"

"""
import logging
logging.basicConfig()
import datetime
import dateutil
import pytz
from django.utils import timezone
from consent.models import BlibbleTest

now = datetime.datetime.now(pytz.utc)
t = BlibbleTest(at=now)
time1 = dateutil.parser.parse("2015-11-11T22:21:37.000000+05:00")
t.save()
# BlibbleTest.objects.filter(at__lt=time1)

# Explicitly use transform:
BlibbleTest.objects.filter(at__utc=time1)
BlibbleTest.objects.filter(at__utc=now)
BlibbleTest.objects.filter(at__utcdate=time1)
BlibbleTest.objects.filter(at__utcdate=now)
BlibbleTest.objects.filter(at__sourcedate=time1)
BlibbleTest.objects.filter(at__sourcedate=now)

# Use 'exact' lookup
BlibbleTest.objects.filter(at=time1)
BlibbleTest.objects.filter(at=now)
"""
