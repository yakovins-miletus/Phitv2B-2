"""Deterministic sample content for Phitopolis Heimdall CMS."""

from datetime import date
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.core.content_status import ContentStatus
from app.db.base import Base
from app.db.seed_content import SEED_BLOG_POSTS as _SCRAPED_BLOG_POSTS
from app.features.blog.models import BlogPost
from app.features.contact.models import ContactMessage
from app.features.services.models import Service
from app.features.team.models import TeamMember

SEED_SERVICES = [
    {
        "slug": "development",
        "name": "Software Development",
        "tagline": "Cloud-native platforms at petabyte scale.",
        "description": (
            "We architect secure, event-driven SaaS platforms with modern stacks, "
            "engineered for enterprise-grade scale and relentless uptime — like the "
            "OmniDashboard portal that lets institutional investors watch billion-dollar "
            "portfolios move in real time."
        ),
        "icon": "hub",
        "highlights": ["TypeScript", "React", "GraphQL", "Docker", "AWS", "CI/CD"],
        "display_order": 1,
        "sub_teams": [
            {"name": "Platform Team", "description": "Architects the core scalable microservices and APIs powering the trading ecosystem."},
            {"name": "Web Apps", "description": "Builds responsive, high-performance user interfaces for real-time portfolio management."},
            {"name": "Infra", "description": "Designs and maintains robust, containerized cloud environments ensuring high availability."},
            {"name": "HPC", "description": "Engineers high-performance computing clusters for executing low-latency market algorithms."}
        ]
    },
    {
        "slug": "quant-research",
        "name": "Quantitative Research",
        "tagline": "Global markets treated as a strict science.",
        "description": (
            "Our researchers turn raw, noisy market data into trading signals. "
            "Pipelines like Project Clairvoyant digest petabytes of historical ticks "
            "and alternative data — from satellite imagery to sentiment — to call "
            "short-term moves with statistical confidence."
        ),
        "icon": "query_stats",
        "highlights": ["Python", "Machine Learning", "Deep Learning", "Statistics"],
        "display_order": 2,
        "sub_teams": [
            {"name": "Alpha Research", "description": "Discovers and tests new predictive signals from complex financial datasets."},
            {"name": "Portfolio Optimization", "description": "Develops algorithms to maximize risk-adjusted returns across broad asset classes."},
            {"name": "Risk Modeling", "description": "Builds robust models to forecast market volatility and mitigate systemic exposure."},
            {"name": "Alternative Data", "description": "Extracts actionable insights from unconventional sources like satellite imagery and web sentiment."}
        ]
    },
    {
        "slug": "data-science",
        "name": "Data Science",
        "tagline": "Pipelines and data lakes that never bottleneck.",
        "description": (
            "We design the ETL backbones and data products researchers and quantitative "
            "traders live on, with rigorous quality gates at every stage so every "
            "downstream signal stands on data that can be trusted."
        ),
        "icon": "model_training",
        "highlights": ["Python", "AWS", "ETL", "Postgres", "NoSQL", "Docker"],
        "display_order": 3,
        "sub_teams": [
            {"name": "Data Engineering", "description": "Constructs scalable pipelines and architectures to ingest and process vast market data."},
            {"name": "ML Ops", "description": "Deploys, monitors, and maintains machine learning models in production environments."},
            {"name": "Analytics", "description": "Transforms complex datasets into intuitive dashboards and actionable business intelligence."},
            {"name": "Core Data", "description": "Manages the central data warehouses and ensures strict governance and data quality."}
        ]
    },
    {
        "slug": "support",
        "name": "Ops Support",
        "tagline": "Follow-the-sun operations that never sleep.",
        "description": (
            "Our global teams keep high-frequency trading platforms, market-data pipelines, "
            "and cloud infrastructure running flawlessly around the clock — an automated SRE "
            "matrix with AI-driven anomaly detection that catches bottlenecks before clients feel them."
        ),
        "icon": "science",
        "highlights": ["Linux", "Prometheus", "Grafana", "AWS / GCP / Azure"],
        "display_order": 4,
        "sub_teams": [
            {"name": "Site Reliability (SRE)", "description": "Ensures maximum uptime and performance through automated recovery and monitoring."},
            {"name": "Trade Ops", "description": "Provides round-the-clock support for live trading systems and market connectivity."},
            {"name": "Security", "description": "Implements stringent security protocols to defend against cyber threats and ensure compliance."},
            {"name": "Global Support", "description": "Delivers immediate, follow-the-sun technical assistance to internal teams and clients."}
        ]
    },
]

SEED_TEAM = [
    {
        "name": "Krizel Mangana",
        "role": "Chief Executive Officer · Co-founder",
        "bio": (
            "Co-founder and CEO. Leads the firm's first-class team of "
            "technologists from Bonifacio Global City, Manila."
        ),
        "focus_areas": ["leadership", "growth"],
        "avatar_seed": "KM",
        "display_order": 1,
    },
    {
        "name": "Mark Walbaum",
        "role": "Chief Technology Officer · Co-founder",
        "bio": (
            "Wall Street engineering leadership at Morgan Stanley, Merrill Lynch, "
            "and JPMorgan; built Manila engineering teams for Deutsche Bank and "
            "Macquarie before co-founding Phitopolis."
        ),
        "focus_areas": ["trading systems", "engineering leadership"],
        "avatar_seed": "MW",
        "display_order": 2,
    },
    {
        "name": "Head of Quantitative Research",
        "role": "Quantitative Research",
        "bio": (
            "Turns high-quality data into deployable trading signals — research, "
            "feature engineering, and quantitative modeling under risk controls."
        ),
        "focus_areas": ["signals", "backtesting"],
        "avatar_seed": "QR",
        "display_order": 3,
    },
    {
        "name": "Head of Data Science & Engineering",
        "role": "Data Science & Engineering",
        "bio": (
            "Statistics, machine learning, and AI against large, noisy data sets "
            "— and the pipelines that feed them, point-in-time correct."
        ),
        "focus_areas": ["machine learning", "data pipelines"],
        "avatar_seed": "DS",
        "display_order": 4,
    },
    {
        "name": "Head of Applications Development",
        "role": "Applications Development",
        "bio": (
            "C++, Python, and MERN systems running in public and private cloud "
            "for global clients — built to trading-infrastructure standards."
        ),
        "focus_areas": ["low-latency systems", "cloud"],
        "avatar_seed": "AD",
        "display_order": 5,
    },
]

SEED_CONTACT_MESSAGES = [
    {
        "name": "Elena Marchetti",
        "email": "elena.marchetti@example-capital.com",
        "subject": "Joint R&D on execution data",
        "message": (
            "We read your execution-cost decomposition note and would like to "
            "discuss a joint research engagement on our execution data."
        ),
    },
    {
        "name": "David Okafor",
        "email": "d.okafor@example-university.edu",
        "subject": "Technical Graduate Program inquiry",
        "message": (
            "Our career office would like to learn more about the two-year "
            "technical graduate program for our quantitative finance students."
        ),
    },
]

SEED_BLOG_POSTS = [
    {
        **row,
        "status": ContentStatus(row["status"]),
        "published_on": date.fromisoformat(row["published_on"]),
    }
    for row in _SCRAPED_BLOG_POSTS
]


async def init_db(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_if_empty(session: AsyncSession) -> None:
    count = await session.scalar(select(func.count()).select_from(Service))
    if count:
        return
    session.add_all([Service(**row) for row in SEED_SERVICES])
    session.add_all([TeamMember(**row) for row in SEED_TEAM])
    session.add_all([ContactMessage(**row) for row in SEED_CONTACT_MESSAGES])
    await session.commit()


async def seed_blog_if_empty(session: AsyncSession) -> None:
    count = await session.scalar(select(func.count()).select_from(BlogPost))
    if count:
        return
    session.add_all([BlogPost(**row) for row in SEED_BLOG_POSTS])
    await session.commit()
