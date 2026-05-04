with services as (
    select distinct
        hcpcs_code,
        hcpcs_description,
        is_drug_service
    from {{ ref('stg_cms_providers') }}
    where hcpcs_code is not null
)

select * from services
