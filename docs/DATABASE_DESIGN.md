# Database Design Document
## GenStudio AI: Relational Schema Specification & Entity-Relationship Model

### 1. Database Architecture Overview
The persistence layer utilizes SQLAlchemy 2.0 with strict relational integrity constraints:
- **Primary Keys:** UUID v4 strings (36 characters) ensuring distributed uniqueness without sequence bottlenecks.
- **Foreign Keys:** Cascading deletes (`CASCADE`) on parent-child relationships (e.g., User -> Projects) and nullification (`SET NULL`) on asset references.
- **Timestamps:** UTC timestamps (`created_at`, `updated_at`) indexed for chronological pagination.
- **Indexing:** High-cardinality foreign keys (`user_id`, `project_id`, `job_id`) and status fields are indexed.

### 2. Entity-Relationship Diagram (Mermaid)

```mermaid
erDiagram
    USERS ||--o{ SESSIONS : has
    USERS ||--o{ PROJECTS : owns
    USERS ||--o{ GENERATION_JOBS : initiates
    USERS ||--o{ MEDIA_ASSETS : owns
    USERS ||--o{ USAGE_RECORDS : incurs
    USERS ||--o{ AUDIT_LOGS : triggers
    
    PROJECTS ||--o{ GENERATION_JOBS : contains
    PROJECTS ||--o{ MEDIA_ASSETS : groups

    GENERATION_JOBS ||--o{ MEDIA_ASSETS : produces
    GENERATION_JOBS ||--o{ USAGE_RECORDS : tracks

    EVALUATION_RUNS ||--o{ EVALUATION_RESULTS : contains

    USERS {
        string id PK "UUID v4"
        string email UK "Unique email address"
        string hashed_password "Argon2id hash"
        string full_name "Display name"
        string role "USER, ADMIN, OWNER"
        boolean is_active "Active account flag"
        datetime created_at
        datetime updated_at
    }

    PROJECTS {
        string id PK "UUID v4"
        string user_id FK "User foreign key"
        string name "Project name"
        text description "Optional description"
        boolean is_archived "Archive flag"
        datetime created_at
        datetime updated_at
    }

    GENERATION_JOBS {
        string id PK "UUID v4"
        string user_id FK "User foreign key"
        string project_id FK "Project foreign key"
        string task_type "text-to-image, text-to-video, etc."
        string provider "huggingface, gemini, etc."
        string model_id "Model registry identifier"
        text prompt "Input textual prompt"
        text negative_prompt "Optional negative prompt"
        json parameters "Aspect ratio, seed, steps"
        string status "pending, processing, completed, failed, cancelled"
        int progress "0 to 100 percentage"
        text error_message "Failure explanation if failed"
        float latency_ms "End-to-end execution latency"
        float cost_usd "Incurred inference cost"
        datetime created_at
        datetime completed_at
    }

    MEDIA_ASSETS {
        string id PK "UUID v4"
        string user_id FK "User foreign key"
        string project_id FK "Project foreign key"
        string job_id FK "Originating job foreign key"
        string media_type "image or video"
        string storage_key "Internal relative storage path"
        string file_path "Physical disk path"
        string public_url "Safe HTTP streaming URL"
        string mime_type "image/png, video/mp4, etc."
        int file_size_bytes "Asset byte length"
        string checksum_sha256 "SHA-256 integrity hash"
        boolean is_favorite "Bookmark toggle"
        json metadata_json "Model metadata"
        datetime created_at
    }

    MODEL_REGISTRY {
        string id PK "UUID v4"
        string provider "huggingface, google, etc."
        string model_id UK "Exact canonical model ID"
        string display_name "Human-friendly label"
        json task_types "Supported tasks list"
        string max_resolution "Maximum output resolution"
        json capabilities_json "Supported parameters"
        json pricing_json "Rate card and check timestamp"
        string license_info "License type"
        boolean is_enabled "Enable/disable toggle"
        datetime updated_at
    }

    EVALUATION_RUNS {
        string id PK "UUID v4"
        string name "Experiment run name"
        string dataset_name "GenStudio-Bench-v1"
        int prompt_count "Total observations"
        json target_models "Compared model IDs"
        string status "pending, running, completed"
        json summary_metrics "Aggregate statistical results"
        datetime created_at
        datetime completed_at
    }

    EVALUATION_RESULTS {
        string id PK "UUID v4"
        string run_id FK "Evaluation run foreign key"
        string prompt_id "Benchmark prompt ID"
        text prompt_text "Prompt string"
        string prompt_category "photorealism, cinematic, etc."
        string model_id "Model evaluated"
        float latency_ms "Measured latency"
        float cost_usd "Measured cost"
        boolean success "Success flag"
        float sim_score "Normalized alignment score"
        float temporal_score "Temporal consistency score"
        datetime created_at
    }
```
