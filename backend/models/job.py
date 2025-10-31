from db import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    posting_date = db.Column(db.String(100), nullable=True)  # Can store "2 days ago" or actual date
    job_type = db.Column(db.String(50), default='Full-time')  # Full-time, Part-time, Contract, Internship
    tags = db.Column(db.Text, nullable=True)  # Comma-separated tags
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert job object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'posting_date': self.posting_date,
            'job_type': self.job_type,
            'tags': self.tags.split(',') if self.tags else [],  # Convert to list
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'