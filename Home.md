# Digital FTE Dashboard

Welcome to the Digital FTE dashboard. This page displays tasks currently in the system.

## Tasks Needing Action
```dataview
TABLE created AS "Created Date"
FROM "02_Needs_Action"
WHERE status = "needs-action"
SORT created DESC
```

## Tasks Pending Approval
```dataview
TABLE created AS "Created Date"
FROM "03_Pending_Approval"
WHERE status = "pending-approval"
SORT created DESC
```

## System Status
- Watching: `01_Inbox` folder
- Last processed: {{last_processed_time}}
- Active tasks: {{active_task_count}}