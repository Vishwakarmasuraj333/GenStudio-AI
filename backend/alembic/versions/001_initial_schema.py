"""Initial GenStudio AI Schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-11-24 11:25:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    # Users
    if 'users' not in existing_tables:
        op.create_table(
            'users',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=False),
            sa.Column('hashed_password', sa.String(length=255), nullable=False),
            sa.Column('full_name', sa.String(length=255), nullable=True),
            sa.Column('role', sa.String(length=20), nullable=False),
            sa.Column('is_active', sa.Boolean(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index('ix_users_email', 'users', ['email'], unique=True)
        op.create_index('ix_users_id', 'users', ['id'], unique=False)

    # Sessions
    if 'sessions' not in existing_tables:
        op.create_table(
            'sessions',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('user_id', sa.String(length=36), nullable=False),
            sa.Column('token_hash', sa.String(length=255), nullable=False),
            sa.Column('ip_address', sa.String(length=50), nullable=True),
            sa.Column('user_agent', sa.String(length=255), nullable=True),
            sa.Column('expires_at', sa.DateTime(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index('ix_sessions_user_id', 'sessions', ['user_id'], unique=False)

    # Projects
    if 'projects' not in existing_tables:
        op.create_table(
            'projects',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('user_id', sa.String(length=36), nullable=False),
            sa.Column('name', sa.String(length=255), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('is_archived', sa.Boolean(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index('ix_projects_user_id', 'projects', ['user_id'], unique=False)

    # Generation Jobs
    if 'generation_jobs' not in existing_tables:
        op.create_table(
            'generation_jobs',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('user_id', sa.String(length=36), nullable=False),
            sa.Column('project_id', sa.String(length=36), nullable=True),
            sa.Column('task_type', sa.String(length=30), nullable=False),
            sa.Column('provider', sa.String(length=50), nullable=False),
            sa.Column('model_id', sa.String(length=100), nullable=False),
            sa.Column('prompt', sa.Text(), nullable=False),
            sa.Column('negative_prompt', sa.Text(), nullable=True),
            sa.Column('parameters', sa.JSON(), nullable=True),
            sa.Column('status', sa.String(length=20), nullable=False),
            sa.Column('progress', sa.Integer(), nullable=True),
            sa.Column('error_message', sa.Text(), nullable=True),
            sa.Column('latency_ms', sa.Float(), nullable=True),
            sa.Column('cost_usd', sa.Float(), nullable=True),
            sa.Column('provider_job_id', sa.String(length=100), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('started_at', sa.DateTime(), nullable=True),
            sa.Column('completed_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index('ix_generation_jobs_user_id', 'generation_jobs', ['user_id'], unique=False)
        op.create_index('ix_generation_jobs_status', 'generation_jobs', ['status'], unique=False)

    # Media Assets
    if 'media_assets' not in existing_tables:
        op.create_table(
            'media_assets',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('user_id', sa.String(length=36), nullable=False),
            sa.Column('project_id', sa.String(length=36), nullable=True),
            sa.Column('job_id', sa.String(length=36), nullable=True),
            sa.Column('media_type', sa.String(length=20), nullable=False),
            sa.Column('storage_key', sa.String(length=255), nullable=False),
            sa.Column('file_path', sa.String(length=500), nullable=False),
            sa.Column('public_url', sa.String(length=500), nullable=False),
            sa.Column('mime_type', sa.String(length=50), nullable=False),
            sa.Column('file_size_bytes', sa.Integer(), nullable=False),
            sa.Column('width', sa.Integer(), nullable=True),
            sa.Column('height', sa.Integer(), nullable=True),
            sa.Column('duration_sec', sa.Float(), nullable=True),
            sa.Column('checksum_sha256', sa.String(length=64), nullable=False),
            sa.Column('is_favorite', sa.Boolean(), nullable=False),
            sa.Column('metadata_json', sa.JSON(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['job_id'], ['generation_jobs.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # Model Registry
    if 'model_registry' not in existing_tables:
        op.create_table(
            'model_registry',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('provider', sa.String(length=50), nullable=False),
            sa.Column('model_id', sa.String(length=100), nullable=False),
            sa.Column('display_name', sa.String(length=100), nullable=False),
            sa.Column('version', sa.String(length=30), nullable=True),
            sa.Column('task_types', sa.JSON(), nullable=False),
            sa.Column('max_resolution', sa.String(length=20), nullable=True),
            sa.Column('supported_aspect_ratios', sa.JSON(), nullable=True),
            sa.Column('capabilities_json', sa.JSON(), nullable=True),
            sa.Column('pricing_json', sa.JSON(), nullable=True),
            sa.Column('license_info', sa.String(length=100), nullable=True),
            sa.Column('is_enabled', sa.Boolean(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('model_id')
        )

    # Evaluation Runs & Results
    if 'evaluation_runs' not in existing_tables:
        op.create_table(
            'evaluation_runs',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('name', sa.String(length=255), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('dataset_name', sa.String(length=100), nullable=False),
            sa.Column('prompt_count', sa.Integer(), nullable=True),
            sa.Column('target_models', sa.JSON(), nullable=True),
            sa.Column('status', sa.String(length=20), nullable=False),
            sa.Column('summary_metrics', sa.JSON(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('completed_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )

    if 'evaluation_results' not in existing_tables:
        op.create_table(
            'evaluation_results',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('run_id', sa.String(length=36), nullable=False),
            sa.Column('prompt_id', sa.String(length=50), nullable=False),
            sa.Column('prompt_text', sa.Text(), nullable=False),
            sa.Column('prompt_category', sa.String(length=50), nullable=False),
            sa.Column('model_id', sa.String(length=100), nullable=False),
            sa.Column('latency_ms', sa.Float(), nullable=False),
            sa.Column('cost_usd', sa.Float(), nullable=True),
            sa.Column('success', sa.Boolean(), nullable=False),
            sa.Column('error_message', sa.Text(), nullable=True),
            sa.Column('output_asset_id', sa.String(length=36), nullable=True),
            sa.Column('human_score_quality', sa.Float(), nullable=True),
            sa.Column('human_score_alignment', sa.Float(), nullable=True),
            sa.Column('sim_score', sa.Float(), nullable=True),
            sa.Column('temporal_score', sa.Float(), nullable=True),
            sa.Column('raw_metrics_json', sa.JSON(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['run_id'], ['evaluation_runs.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # User Feedback
    if 'user_feedback' not in existing_tables:
        op.create_table(
            'user_feedback',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('user_id', sa.String(length=36), nullable=False),
            sa.Column('job_id', sa.String(length=36), nullable=True),
            sa.Column('asset_id', sa.String(length=36), nullable=True),
            sa.Column('rating', sa.Integer(), nullable=False),
            sa.Column('feedback_text', sa.Text(), nullable=True),
            sa.Column('tags', sa.JSON(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['asset_id'], ['media_assets.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['job_id'], ['generation_jobs.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # Usage Records
    if 'usage_records' not in existing_tables:
        op.create_table(
            'usage_records',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('user_id', sa.String(length=36), nullable=False),
            sa.Column('job_id', sa.String(length=36), nullable=True),
            sa.Column('provider', sa.String(length=50), nullable=False),
            sa.Column('model_id', sa.String(length=100), nullable=False),
            sa.Column('prompt_tokens', sa.Integer(), nullable=True),
            sa.Column('completion_tokens', sa.Integer(), nullable=True),
            sa.Column('compute_duration_sec', sa.Float(), nullable=True),
            sa.Column('estimated_cost_usd', sa.Float(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['job_id'], ['generation_jobs.id'], ondelete='SET NULL'),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id')
        )

    # Audit Logs
    if 'audit_logs' not in existing_tables:
        op.create_table(
            'audit_logs',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('user_id', sa.String(length=36), nullable=True),
            sa.Column('action', sa.String(length=100), nullable=False),
            sa.Column('resource_type', sa.String(length=50), nullable=False),
            sa.Column('resource_id', sa.String(length=100), nullable=True),
            sa.Column('details_json', sa.JSON(), nullable=True),
            sa.Column('ip_address', sa.String(length=50), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
            sa.PrimaryKeyConstraint('id')
        )

def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('usage_records')
    op.drop_table('user_feedback')
    op.drop_table('evaluation_results')
    op.drop_table('evaluation_runs')
    op.drop_table('model_registry')
    op.drop_table('media_assets')
    op.drop_table('generation_jobs')
    op.drop_table('projects')
    op.drop_table('sessions')
    op.drop_table('users')
