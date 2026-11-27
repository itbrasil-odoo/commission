# Copyright 2026 IT Brasil
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


def migrate(cr, version):
    """Databases still below 19.0.2.0.0 skipped the rename of
    res.partner.agent_ids to commission_agent_ids (its 19.0 script was dropped
    with the 20.0 migration). Rename the field metadata so the ORM keeps the
    field instead of deleting it and breaking filters and exports."""
    if not version or tuple(int(x) for x in version.split(".")[2:5]) >= (2, 0, 0):
        return
    cr.execute(
        """
        SELECT 1 FROM ir_model_fields
         WHERE model = 'res.partner' AND name = 'commission_agent_ids'
        """
    )
    if cr.fetchone():
        return
    cr.execute(
        """
        UPDATE ir_model_fields
           SET name = 'commission_agent_ids'
         WHERE model = 'res.partner' AND name = 'agent_ids'
        """
    )
    cr.execute(
        """
        UPDATE ir_model_data
           SET name = 'field_res_partner__commission_agent_ids'
         WHERE module = 'commission_oca'
           AND name = 'field_res_partner__agent_ids'
        """
    )
