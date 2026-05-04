with providers as (
    select distinct
        npi,
        provider_last_org_name,
        provider_first_name,
        provider_mi,
        provider_credentials,
        entity_code,
        provider_type,
        medicare_participating
    from {{ ref('stg_cms_providers') }}
)

select * from providers
