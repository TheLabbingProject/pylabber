from typing import Dict

from external_tables.sync.subjects import SubjectsSynchronizer
from external_tables.sync.synchronizer import Synchronizer

MODEL_SYNCHRONIZER: Dict[str, Synchronizer] = {
    "research | subject": SubjectsSynchronizer
}
