import sqlite3
from pathlib import Path

from backend.database.models import (
    CaseRecord,
    EventRecord,
    FirstAppealRecord,
)
from backend.database.storage import StorageBackend
from backend.models.case import Case
from backend.models.event import CaseEvent


class LocalStore(StorageBackend):

    def __init__(
        self,
        db_path: str | Path = "data/civivos.db"
    ):

        self.db_path = Path(db_path)

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._initialize_database()

    # ==================================================
    # DATABASE CONNECTION
    # ==================================================

    def _connect(self):

        connection = sqlite3.connect(
            self.db_path
        )

        connection.row_factory = sqlite3.Row

        return connection

    # ==================================================
    # DATABASE INITIALIZATION
    # ==================================================

    def _initialize_database(self):

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS cases (
                    case_id TEXT PRIMARY KEY,
                    citizen_name TEXT NOT NULL,
                    complaint TEXT NOT NULL,
                    department TEXT NOT NULL,
                    legal_route TEXT NOT NULL,
                    state TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    deadline TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    event TEXT NOT NULL,
                    description TEXT,
                    FOREIGN KEY(case_id)
                        REFERENCES cases(case_id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS first_appeals (
                    appeal_id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL UNIQUE,
                    citizen_name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    legal_route TEXT NOT NULL,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(case_id)
                        REFERENCES cases(case_id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_events_case_id
                ON events(case_id)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_cases_state
                ON cases(state)
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_first_appeals_case_id
                ON first_appeals(case_id)
                """
            )

            connection.commit()

    # ==================================================
    # CASE OPERATIONS
    # ==================================================

    def add_case(
        self,
        case: Case
    ) -> None:

        record = CaseRecord(
            case_id=case.case_id,
            citizen_name=case.citizen_name,
            complaint=case.complaint,
            department=case.department,
            legal_route=case.legal_route,
            state=case.state.value,
            created_at=case.created_at,
            last_updated=case.last_updated,
            deadline=case.deadline
        )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO cases (
                    case_id,
                    citizen_name,
                    complaint,
                    department,
                    legal_route,
                    state,
                    created_at,
                    last_updated,
                    deadline
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.case_id,
                    record.citizen_name,
                    record.complaint,
                    record.department,
                    record.legal_route,
                    record.state,
                    record.created_at.isoformat(),
                    record.last_updated.isoformat(),
                    record.deadline.isoformat()
                )
            )

            connection.commit()

    def update_case(
        self,
        case: Case
    ) -> None:

        record = CaseRecord(
            case_id=case.case_id,
            citizen_name=case.citizen_name,
            complaint=case.complaint,
            department=case.department,
            legal_route=case.legal_route,
            state=case.state.value,
            created_at=case.created_at,
            last_updated=case.last_updated,
            deadline=case.deadline
        )

        with self._connect() as connection:

            cursor = connection.execute(
                """
                UPDATE cases
                SET
                    citizen_name = ?,
                    complaint = ?,
                    department = ?,
                    legal_route = ?,
                    state = ?,
                    created_at = ?,
                    last_updated = ?,
                    deadline = ?
                WHERE case_id = ?
                """,
                (
                    record.citizen_name,
                    record.complaint,
                    record.department,
                    record.legal_route,
                    record.state,
                    record.created_at.isoformat(),
                    record.last_updated.isoformat(),
                    record.deadline.isoformat(),
                    record.case_id
                )
            )

            if cursor.rowcount == 0:

                raise ValueError(
                    f"Case '{case.case_id}' does not exist."
                )

            connection.commit()

    def get_case(
        self,
        case_id: str
    ) -> Case | None:

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT
                    case_id,
                    citizen_name,
                    complaint,
                    department,
                    legal_route,
                    state,
                    created_at,
                    last_updated,
                    deadline
                FROM cases
                WHERE case_id = ?
                """,
                (case_id,)
            ).fetchone()

        if row is None:
            return None

        return self._row_to_case(row)

    def get_all_cases(
        self
    ) -> list[Case]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT
                    case_id,
                    citizen_name,
                    complaint,
                    department,
                    legal_route,
                    state,
                    created_at,
                    last_updated,
                    deadline
                FROM cases
                ORDER BY created_at ASC
                """
            ).fetchall()

        return [
            self._row_to_case(row)
            for row in rows
        ]

    def get_waiting_response_cases(
        self
    ) -> list[Case]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT
                    case_id,
                    citizen_name,
                    complaint,
                    department,
                    legal_route,
                    state,
                    created_at,
                    last_updated,
                    deadline
                FROM cases
                WHERE state = ?
                ORDER BY deadline ASC
                """,
                ("WAITING_RESPONSE",)
            ).fetchall()

        return [
            self._row_to_case(row)
            for row in rows
        ]

    # ==================================================
    # CASE ROW CONVERSION
    # ==================================================

    def _row_to_case(
        self,
        row
    ) -> Case:

        record = CaseRecord(
            case_id=row["case_id"],
            citizen_name=row["citizen_name"],
            complaint=row["complaint"],
            department=row["department"],
            legal_route=row["legal_route"],
            state=row["state"],
            created_at=row["created_at"],
            last_updated=row["last_updated"],
            deadline=row["deadline"]
        )

        return Case(
            case_id=record.case_id,
            citizen_name=record.citizen_name,
            complaint=record.complaint,
            department=record.department,
            legal_route=record.legal_route,
            state=record.state,
            created_at=record.created_at,
            last_updated=record.last_updated,
            deadline=record.deadline
        )

    # ==================================================
    # EVENT OPERATIONS
    # ==================================================

    def add_event(
        self,
        case_id: str,
        event: CaseEvent
    ) -> None:

        if self.get_case(case_id) is None:

            raise ValueError(
                f"Cannot add event. "
                f"Case '{case_id}' does not exist."
            )

        record = EventRecord(
            event_id=event.event_id,
            case_id=case_id,
            timestamp=event.timestamp,
            event=event.event,
            description=event.description
        )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO events (
                    event_id,
                    case_id,
                    timestamp,
                    event,
                    description
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    record.event_id,
                    record.case_id,
                    record.timestamp.isoformat(),
                    record.event,
                    record.description
                )
            )

            connection.commit()

    def get_timeline(
        self,
        case_id: str
    ) -> list[CaseEvent]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT
                    event_id,
                    case_id,
                    timestamp,
                    event,
                    description
                FROM events
                WHERE case_id = ?
                ORDER BY timestamp ASC
                """,
                (case_id,)
            ).fetchall()

        events: list[CaseEvent] = []

        for row in rows:

            record = EventRecord(
                event_id=row["event_id"],
                case_id=row["case_id"],
                timestamp=row["timestamp"],
                event=row["event"],
                description=row["description"]
            )

            events.append(
                CaseEvent(
                    event_id=record.event_id,
                    timestamp=record.timestamp,
                    event=record.event,
                    description=record.description
                )
            )

        return events

    # ==================================================
    # FIRST APPEAL OPERATIONS
    # ==================================================

    def add_first_appeal(
        self,
        appeal
    ) -> None:

        record = FirstAppealRecord(
            appeal_id=appeal.appeal_id,
            case_id=appeal.case_id,
            citizen_name=appeal.citizen_name,
            department=appeal.department,
            legal_route=appeal.legal_route,
            title=appeal.title,
            body=appeal.body,
            created_at=appeal.created_at
        )

        if self.get_case(record.case_id) is None:

            raise ValueError(
                f"Cannot add appeal. "
                f"Case '{record.case_id}' does not exist."
            )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO first_appeals (
                    appeal_id,
                    case_id,
                    citizen_name,
                    department,
                    legal_route,
                    title,
                    body,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.appeal_id,
                    record.case_id,
                    record.citizen_name,
                    record.department,
                    record.legal_route,
                    record.title,
                    record.body,
                    record.created_at.isoformat()
                )
            )

            connection.commit()

    def get_first_appeal(
        self,
        case_id: str
    ):

        from backend.appeal_models import FirstAppeal

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT
                    appeal_id,
                    case_id,
                    citizen_name,
                    department,
                    legal_route,
                    title,
                    body,
                    created_at
                FROM first_appeals
                WHERE case_id = ?
                """,
                (case_id,)
            ).fetchone()

        if row is None:
            return None

        return FirstAppeal(
            appeal_id=row["appeal_id"],
            case_id=row["case_id"],
            citizen_name=row["citizen_name"],
            department=row["department"],
            legal_route=row["legal_route"],
            title=row["title"],
            body=row["body"],
            created_at=row["created_at"]
        )