########################
# Groups & Permissions #
########################

PERMISSIONS_GROUPS = {
    "MANAGER_GENERAL": [
        "add_association",
        "add_association_any_institution",
        "change_association",
        "change_association_any_institution",
        "change_association_all_fields",
        "delete_association",
        "delete_association_any_institution",
        "view_association_not_enabled",
        "view_association_not_public",
        "add_user",
        "add_user_misc",
        "change_user",
        "change_user_misc",
        "delete_user",
        "delete_user_misc",
        "view_user",
        "view_user_misc",
        "view_user_anyone",
        "change_associationusers",
        "change_associationusers_any_institution",
        "delete_associationusers",
        "delete_associationusers_any_institution",
        "view_associationusers",
        "view_associationusers_anyone",
        "add_groupinstitutioncommissionusers_any_group",
        "delete_groupinstitutioncommissionusers",
        "delete_groupinstitutioncommissionusers_any_group",
        "view_groupinstitutioncommissionusers",
        "view_groupinstitutioncommissionusers_any_group",
        "add_document",
        "delete_document",
        "delete_document_any_institution",
    ],
    "MANAGER_INSTITUTION": [
        "add_association",
        "change_association",
        "change_association_all_fields",
        "delete_association",
        "view_association_not_enabled",
        "view_association_not_public",
        "add_user",
        "change_user",
        "delete_user",
        "view_user",
        "view_user_anyone",
        "change_associationusers",
        "delete_associationusers",
        "view_associationusers",
        "view_associationusers_anyone",
        "delete_groupinstitutioncommissionusers",
        "view_groupinstitutioncommissionusers",
        "view_groupinstitutioncommissionusers_any_group",
        "add_document",
        "delete_document",
    ],
    "MANAGER_MISC": [
        "add_association",
        "change_association",
        "change_association_all_fields",
        "delete_association",
        "view_association_not_enabled",
        "view_association_not_public",
        "add_user",
        "add_user_misc",
        "change_user",
        "change_user_misc",
        "delete_user",
        "delete_user_misc",
        "view_user",
        "view_user_misc",
        "change_associationusers",
        "delete_associationusers",
        "view_associationusers",
        "view_associationusers_anyone",
        "delete_groupinstitutioncommissionusers",
        "view_groupinstitutioncommissionusers",
        "view_groupinstitutioncommissionusers_any_group",
    ],
    "COMMISSION": [
        "view_association_not_public",
        "view_user",
        "view_user_misc",
        "view_user_anyone",
        "view_associationusers",
        "view_groupinstitutioncommissionusers",
    ],
    "STUDENT_INSTITUTION": [
        "change_association",
        "view_user",
        "change_associationusers",
        "delete_associationusers",
        "view_associationusers",
        "view_groupinstitutioncommissionusers",
    ],
    "STUDENT_MISC": [
        "view_groupinstitutioncommissionusers",
    ],
}
