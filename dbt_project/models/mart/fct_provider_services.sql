with base as (
    select
        npi,
        hcpcs_code,
        state,
        provider_type,
        place_of_service,
        total_beneficiaries,
        total_services,
        total_beneficiary_day_services,
        avg_submitted_charge,
        avg_medicare_allowed_amount,
        avg_medicare_payment_amount,
        avg_medicare_standardized_amount,
        -- derived metrics relevant to claims analytics
        round(
            case
                when avg_submitted_charge > 0
                then avg_medicare_payment_amount / avg_submitted_charge
                else null
            end,
            4
        ) as payment_to_charge_ratio,
        round(avg_submitted_charge - avg_medicare_payment_amount, 2) as avg_denied_amount
    from {{ ref('stg_cms_providers') }}
    where total_services > 0
)

select * from base
