with source as (
    select * from {{ source('raw', 'CMS_MEDICARE_PROVIDERS') }}
),

renamed as (
    select
        "Rndrng_NPI"                    as npi,
        "Rndrng_Prvdr_Last_Org_Name"    as provider_last_org_name,
        "Rndrng_Prvdr_First_Name"       as provider_first_name,
        "Rndrng_Prvdr_MI"               as provider_mi,
        "Rndrng_Prvdr_Crdntls"          as provider_credentials,
        "Rndrng_Prvdr_Ent_Cd"           as entity_code,
        "Rndrng_Prvdr_St1"              as address_line_1,
        "Rndrng_Prvdr_St2"              as address_line_2,
        "Rndrng_Prvdr_City"             as city,
        "Rndrng_Prvdr_State_Abrvtn"     as state,
        "Rndrng_Prvdr_State_FIPS"       as state_fips,
        "Rndrng_Prvdr_Zip5"             as zip_code,
        "Rndrng_Prvdr_RUCA"             as ruca_code,
        "Rndrng_Prvdr_RUCA_Desc"        as ruca_description,
        "Rndrng_Prvdr_Cntry"            as country,
        "Rndrng_Prvdr_Type"             as provider_type,
        "Rndrng_Prvdr_Mdcr_Prtcptg_Ind" as medicare_participating,
        "HCPCS_Cd"                      as hcpcs_code,
        "HCPCS_Desc"                    as hcpcs_description,
        "HCPCS_Drug_Ind"                as is_drug_service,
        "Place_Of_Srvc"                 as place_of_service,
        try_to_number("Tot_Benes")      as total_beneficiaries,
        try_to_number("Tot_Srvcs")      as total_services,
        try_to_number("Tot_Bene_Day_Srvcs") as total_beneficiary_day_services,
        try_to_number("Avg_Sbmtd_Chrg", 18, 2) as avg_submitted_charge,
        try_to_number("Avg_Mdcr_Alowd_Amt", 18, 2) as avg_medicare_allowed_amount,
        try_to_number("Avg_Mdcr_Pymt_Amt", 18, 2) as avg_medicare_payment_amount,
        try_to_number("Avg_Mdcr_Stdzd_Amt", 18, 2) as avg_medicare_standardized_amount
    from source
    where "Rndrng_NPI" is not null
      and "HCPCS_Cd" is not null
)

select * from renamed
