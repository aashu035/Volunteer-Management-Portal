"""
Database seed script — populates demo data for all three roles.

Run with: python -m app.db.seed
"""

import asyncio
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.db.base import Base, engine
from app.db.session import async_session_factory
from app.models.user import User, UserRole, UserStatus
from app.models.volunteer import VolunteerProfile
from app.models.skill import Skill, VolunteerSkill, SkillProficiency
from app.models.event import Event, EventStatus, EventSkill, EventRegistration
from app.models.task import Task, TaskStatus
from app.models.notification import Notification, NotificationType


async def seed():
    """Seed the database with demo data."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        print("🌱 Seeding database...")

        # --- Skills ---
        skills_data = [
            ("First Aid", "Medical"),
            ("Event Planning", "Organization"),
            ("Teaching", "Education"),
            ("Python", "Technical"),
            ("JavaScript", "Technical"),
            ("Photography", "Creative"),
            ("Cooking", "Culinary"),
            ("Public Speaking", "Communication"),
            ("Driving", "Logistics"),
            ("Social Media", "Marketing"),
        ]
        skills = {}
        for name, category in skills_data:
            skill = Skill(name=name, category=category)
            session.add(skill)
            skills[name] = skill
        await session.flush()
        print(f"  ✅ Created {len(skills)} skills")

        # --- Admin User ---
        admin_hash = await hash_password("Admin@123")
        admin = User(
            email="admin@amaanitvam.org",
            password_hash=admin_hash,
            full_name="Admin User",
            phone="+919876543210",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
        )
        session.add(admin)
        await session.flush()
        print("  ✅ Created admin user")

        # --- Coordinator User ---
        coord_hash = await hash_password("Coord@123")
        coordinator = User(
            email="coordinator@amaanitvam.org",
            password_hash=coord_hash,
            full_name="Priya Sharma",
            phone="+919876543211",
            role=UserRole.COORDINATOR,
            status=UserStatus.ACTIVE,
        )
        session.add(coordinator)
        await session.flush()
        print("  ✅ Created coordinator user")

        # --- Volunteer Users ---
        volunteers = []
        volunteer_data = [
            ("volunteer@amaanitvam.org", "Rahul Verma", "+919876543212"),
            ("anita@amaanitvam.org", "Anita Gupta", "+919876543213"),
            ("deepak@amaanitvam.org", "Deepak Kumar", "+919876543214"),
            ("sneha@amaanitvam.org", "Sneha Patel", "+919876543215"),
            ("arjun@amaanitvam.org", "Arjun Singh", "+919876543216"),
        ]
        vol_hash = await hash_password("Vol@123")
        for email, name, phone in volunteer_data:
            vol = User(
                email=email,
                password_hash=vol_hash,
                full_name=name,
                phone=phone,
                role=UserRole.VOLUNTEER,
                status=UserStatus.ACTIVE,
            )
            session.add(vol)
            volunteers.append(vol)
        await session.flush()
        print(f"  ✅ Created {len(volunteers)} volunteer users")

        # --- Volunteer Profiles ---
        profiles = []
        bios = [
            "Passionate about education and community development.",
            "Technology enthusiast helping NGOs go digital.",
            "Medical student volunteering during weekends.",
            "Professional photographer supporting social causes.",
            "Fitness trainer organizing health camps for rural communities.",
        ]
        locations = ["Delhi", "Mumbai", "Bangalore", "Pune", "Chennai"]
        for i, vol in enumerate(volunteers):
            profile = VolunteerProfile(
                user_id=vol.id,
                bio=bios[i],
                location=locations[i],
                total_hours=[120.5, 85.0, 45.0, 200.0, 15.0][i],
            )
            session.add(profile)
            profiles.append(profile)
        await session.flush()
        print(f"  ✅ Created {len(profiles)} volunteer profiles")

        # --- Volunteer Skills ---
        skill_assignments = [
            (0, ["Teaching", "Public Speaking", "First Aid"]),
            (1, ["Python", "JavaScript", "Social Media"]),
            (2, ["First Aid", "Cooking"]),
            (3, ["Photography", "Event Planning", "Social Media"]),
            (4, ["Driving", "Cooking", "First Aid"]),
        ]
        proficiencies = [SkillProficiency.EXPERT, SkillProficiency.INTERMEDIATE, SkillProficiency.BEGINNER]
        for vol_idx, skill_names in skill_assignments:
            for j, skill_name in enumerate(skill_names):
                vs = VolunteerSkill(
                    volunteer_id=profiles[vol_idx].id,
                    skill_id=skills[skill_name].id,
                    proficiency=proficiencies[j % 3],
                    verified=j == 0,
                )
                session.add(vs)
        await session.flush()
        print("  ✅ Assigned skills to volunteers")

        # --- Events ---
        now = datetime.now(timezone.utc)
        events_data = [
            ("Project Shiksha - Mentorship Drive", "Weekly mentorship for underprivileged children in government schools.", "Government School, Sector 14", EventStatus.OPEN, 30),
            ("Environmental Protection Campaign", "Tree plantation and plastic waste cleanup drive across the city.", "City Park", EventStatus.OPEN, 50),
            ("Community Health Camp", "Free health checkups, hygiene kits, and awareness drive for rural communities.", "Village Community Center", EventStatus.IN_PROGRESS, 25),
            ("Women Empowerment Workshop", "Skill development and financial literacy workshop for women.", "Amaanitvam Center", EventStatus.PLANNING, 40),
            ("Food & Blanket Distribution", "Winter distribution drive for the homeless.", "Railway Station Area", EventStatus.COMPLETED, 20),
        ]
        events = []
        for i, (title, desc, loc, status, max_vol) in enumerate(events_data):
            event = Event(
                title=title,
                description=desc,
                location=loc,
                start_date=now + timedelta(days=i * 7),
                end_date=now + timedelta(days=i * 7 + 2),
                max_volunteers=max_vol,
                status=status,
                coordinator_id=coordinator.id,
            )
            session.add(event)
            events.append(event)
        await session.flush()
        print(f"  ✅ Created {len(events)} events")

        # --- Event Skills ---
        event_skill_map = [
            (0, ["First Aid", "Cooking"]),
            (1, ["Teaching", "Public Speaking"]),
            (2, ["Driving"]),
            (3, ["Python", "JavaScript"]),
            (4, ["Cooking", "Driving"]),
        ]
        for evt_idx, skill_names in event_skill_map:
            for sn in skill_names:
                es = EventSkill(event_id=events[evt_idx].id, skill_id=skills[sn].id)
                session.add(es)
        await session.flush()
        print("  ✅ Assigned required skills to events")

        # --- Event Registrations ---
        for vol in volunteers[:3]:
            reg = EventRegistration(event_id=events[0].id, volunteer_id=vol.id)
            session.add(reg)
        for vol in volunteers[1:4]:
            reg = EventRegistration(event_id=events[1].id, volunteer_id=vol.id)
            session.add(reg)
        await session.flush()
        print("  ✅ Created event registrations")

        # --- Tasks ---
        tasks_data = [
            (0, "Set up medical stations", ["First Aid"], 4.0, TaskStatus.PENDING),
            (0, "Prepare awareness pamphlets", ["Public Speaking"], 2.0, TaskStatus.IN_PROGRESS),
            (1, "Prepare lesson plans", ["Teaching"], 3.0, TaskStatus.PENDING),
            (2, "Organize cleanup supplies", ["Driving"], 2.0, TaskStatus.COMPLETED),
            (3, "Set up dev environments", ["Python", "JavaScript"], 1.5, TaskStatus.PENDING),
        ]
        tasks = []
        for evt_idx, title, req_skills, est_hours, status in tasks_data:
            task = Task(
                event_id=events[evt_idx].id,
                title=title,
                required_skills=req_skills,
                estimated_hours=est_hours,
                status=status,
                assigned_to=volunteers[0].id if status != TaskStatus.PENDING else None,
                deadline=now + timedelta(days=evt_idx * 7 - 1),
            )
            session.add(task)
            tasks.append(task)
        await session.flush()
        print(f"  ✅ Created {len(tasks)} tasks")

        # --- Notifications ---
        notifs = [
            (volunteers[0].id, NotificationType.TASK_ASSIGNED, "Task Assigned", "You have been assigned to 'Prepare awareness pamphlets'"),
            (volunteers[1].id, NotificationType.EVENT_REMINDER, "Event Reminder", "Education Workshop starts in 7 days!"),
            (coordinator.id, NotificationType.GENERAL, "New Registration", "Rahul Verma registered for Community Health Camp"),
        ]
        for user_id, ntype, title, message in notifs:
            n = Notification(user_id=user_id, type=ntype, title=title, message=message)
            session.add(n)
        await session.flush()
        print("  ✅ Created notifications")

        await session.commit()
        print("\n🎉 Database seeded successfully!")
        print("   Admin:       admin@amaanitvam.org / Admin@123")
        print("   Coordinator: coordinator@amaanitvam.org / Coord@123")
        print("   Volunteer:   volunteer@amaanitvam.org / Vol@123")


if __name__ == "__main__":
    asyncio.run(seed())
