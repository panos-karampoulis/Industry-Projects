# ==========================================================
# ENTSO-E QUERY BUILDERS
# Energy Trading Decision Support System
# ==========================================================


# ==========================================================
# DOCUMENT TYPES
# ==========================================================

DAY_AHEAD_PRICES = "A44"

LOAD = "A65"

GENERATION = "A74"



# ==========================================================
# PROCESS TYPES
# ==========================================================

DAY_AHEAD_PROCESS = "A01"

REALIZED_PROCESS = "A16"



# ==========================================================
# QUERY BUILDER
# ==========================================================


def build_query(
    security_token,
    document_type,
    process_type,
    domain,
    start,
    end
):


    period_start = (
        start
        .strftime("%Y%m%d%H%M")
    )


    period_end = (
        end
        .strftime("%Y%m%d%H%M")
    )



    params = {


        "securityToken":
            security_token,


        "documentType":
            document_type,


        "processType":
            process_type,


        # ==================================================
        # DOMAIN FIX
        # ==================================================

        "in_Domain":
            domain,


        "out_Domain":
            domain,


        "periodStart":
            period_start,


        "periodEnd":
            period_end

    }


    return params



# ==========================================================
# LOAD
# ==========================================================


def build_load_query(
    token,
    domain,
    start,
    end
):


    return build_query(

        security_token=token,

        document_type=LOAD,

        process_type="A16",

        domain=domain,

        start=start,

        end=end

    )



# ==========================================================
# DAY AHEAD PRICE
# ==========================================================


def build_price_query(
    token,
    domain,
    start,
    end
):


    return build_query(

        security_token=token,

        document_type=DAY_AHEAD_PRICES,

        process_type=DAY_AHEAD_PROCESS,

        domain=domain,

        start=start,

        end=end

    )



# ==========================================================
# GENERATION
# ==========================================================


def build_generation_query(
    token,
    domain,
    start,
    end
):


    return build_query(

        security_token=token,

        document_type=GENERATION,

        process_type=REALIZED_PROCESS,

        domain=domain,

        start=start,

        end=end

    )