# System Diagrams and Workflow Documentation

This file documents the main system diagrams for the Cyber Crime Reporting System, including user roles, use cases, architecture, system components, and working flow.

## 1. User/Actor Diagram

```mermaid
flowchart LR
    Citizen["Citizen / Reporter"]
    Officer["Law Enforcement Officer"]
    Admin["System Admin"]
    System["Cyber Crime Reporting System"]
    Citizen -->|Submit complaint| System
    Citizen -->|Track complaint status| System
    Officer -->|Login to officer portal| System
    Officer -->|Review complaints| System
    Officer -->|Record decisions| System
    Admin -->|Maintain app/configs| System
```

## 2. Use Case Diagram

```mermaid
flowchart TB
    subgraph Actors
        A[Citizen]
        B[Officer]
        C[Admin]
    end

    subgraph UseCases
        U1[Submit Complaint]
        U2[Upload Evidence]
        U3[Track Complaint]
        U4[Search Cyber Laws]
        U5[Officer Login]
        U6[Review Complaint]
        U7[Record Decision]
        U8[View Statistics]
        U9[Manage Officers]
    end

    A --> U1
    A --> U2
    A --> U3
    A --> U4
    B --> U5
    B --> U6
    B --> U7
    B --> U8
    C --> U9
    C --> U8
```

## 3. Architecture Diagram

```mermaid
flowchart LR
    subgraph Frontend
        FE["Streamlit App\n(frontend/app.py)"]
    end
    subgraph Backend
        BE["Backend API\n(backend/api/main.py)"]
        DB["Database / JSON data files"]
    end
    subgraph Storage
        Files["Evidence Storage / File System"]
    end

    User["User / Officer"] --> FE
    FE --> BE
    BE --> DB
    FE --> Files
    BE --> Files
```

## 4. System Diagram

```mermaid
flowchart TB
    User["User / Reporter"]
    Streamlit["Streamlit Frontend"]
    Pages["Pages Module\n(report_form, tracking, law_guide, help, officer_login, officer_panel)"]
    Data["Data Store\n(JSON + backend data files)"]
    Officer["Officer Decision Workflow"]

    User --> Streamlit
    Streamlit --> Pages
    Pages --> Data
    Officer --> Pages
    Officer --> Data
```

## 5. Working Flow Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Streamlit UI
    participant App as App Router
    participant Data as Data Store
    U->>UI: Open app
    UI->>App: Select page / submit form
    App->>UI: Load page content
    U->>UI: Submit complaint
    UI->>Data: Save complaint JSON
    Data-->>UI: Confirmation
    UI-->>U: Show tracking ID
    U->>UI: Track complaint
    UI->>Data: Query complaint status
    Data-->>UI: Return status
    UI-->>U: Display result
```

## Notes

- The diagrams are intentionally simplified for documentation and architecture planning.
- The app uses JSON-based local data storage for complaint and officer records.
- The frontend routes pages through a session-state-based single-page router.
- Uploaded evidence is managed by the frontend and persisted as secure evidence files in storage.
