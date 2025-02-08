# coding: utf-8

"""
    Lead Scraping Service API

    Vector Lead Scraping Service API - Manages Lead Scraping Jobs

    The version of the OpenAPI document: 1.0
    Contact: yoanyomba@vector.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class BackgroundJobStatus(str, Enum):
    """
    BackgroundJobStatus represents the possible states of a background job. This enum is used to track the lifecycle of asynchronous tasks like scraping jobs.  State transitions: 1. QUEUED -> IN_PROGRESS 2. IN_PROGRESS -> COMPLETED/FAILED/CANCELLED/TIMED_OUT  Usage example: ```go job := &ScrapingJob{     Status: BackgroundJobStatus_BACKGROUND_JOB_STATUS_IN_PROGRESS, } ```   - BACKGROUND_JOB_STATUS_UNSPECIFIED: Default state, should not be used explicitly  - BACKGROUND_JOB_STATUS_QUEUED: Job is queued and waiting to be processed  - BACKGROUND_JOB_STATUS_IN_PROGRESS: Job is currently being processed  - BACKGROUND_JOB_STATUS_COMPLETED: Job has completed successfully  - BACKGROUND_JOB_STATUS_FAILED: Job encountered an error and failed  - BACKGROUND_JOB_STATUS_CANCELLED: Job was manually cancelled by user  - BACKGROUND_JOB_STATUS_TIMED_OUT: Job exceeded its maximum execution time
    """

    """
    allowed enum values
    """
    BACKGROUND_JOB_STATUS_UNSPECIFIED = 'BACKGROUND_JOB_STATUS_UNSPECIFIED'
    BACKGROUND_JOB_STATUS_QUEUED = 'BACKGROUND_JOB_STATUS_QUEUED'
    BACKGROUND_JOB_STATUS_IN_PROGRESS = 'BACKGROUND_JOB_STATUS_IN_PROGRESS'
    BACKGROUND_JOB_STATUS_COMPLETED = 'BACKGROUND_JOB_STATUS_COMPLETED'
    BACKGROUND_JOB_STATUS_FAILED = 'BACKGROUND_JOB_STATUS_FAILED'
    BACKGROUND_JOB_STATUS_CANCELLED = 'BACKGROUND_JOB_STATUS_CANCELLED'
    BACKGROUND_JOB_STATUS_TIMED_OUT = 'BACKGROUND_JOB_STATUS_TIMED_OUT'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of BackgroundJobStatus from a JSON string"""
        return cls(json.loads(json_str))


