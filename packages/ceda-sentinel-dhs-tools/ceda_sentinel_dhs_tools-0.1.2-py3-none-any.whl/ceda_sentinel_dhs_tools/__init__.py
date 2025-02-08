from typing import Dict, Optional, Tuple

from ceda_sentinel_dhs_tools.create_producer_consumer import (
    create_producer_consumer_function,
)
from ceda_sentinel_dhs_tools.delete_producer_consumer import (
    delete_producer_consumer_function,
)
from ceda_sentinel_dhs_tools.list_producer_consumers import list_producers_and_consumers


def list_producer_consumers(
    local_config: str,
    filter_string: Optional[str] = None,
    hours_behind: Optional[int] = None,
    email: Optional[str] = None,
    full_details: Optional[str] = None,
) -> None:
    """List producers and consumers from GSS instance"""
    return list_producers_and_consumers(
        local_config=local_config,
        filter_string=filter_string,
        hours_behind=hours_behind,
        email=email,
        full_details=full_details,
    )


def create_producer_consumer(
    template_base: str,
    config_file: str,
    local_config: str,
    filter_string: Optional[str] = None,
    last_publication_date: Optional[str] = None,
) -> Tuple[Dict, Dict]:
    """Create a new producer/consumer pair"""
    return create_producer_consumer_function(
        template_base=template_base,
        config_file=config_file,
        local_config=local_config,
        filter_string=filter_string,
        last_publication_date=last_publication_date,
    )


def delete_producer_consumer(
    local_config: str,
    base_name: str,
) -> bool:
    """Delete a producer/consumer pair"""
    return delete_producer_consumer_function(
        local_config=local_config,
        base_name=base_name,
    )


__all__ = [
    "list_producer_consumers",
    "create_producer_consumer",
    "delete_producer_consumer",
]
