from flask import Blueprint, request, jsonify
from db import db
from models.job import Job
from sqlalchemy import or_, desc, asc

job_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

# CREATE Add a new job
@job_bp.route('', methods=['POST'])
def create_job():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'company', 'location']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Handle tags convert list to comma separated string if needed
        tags = data.get('tags', '')
        if isinstance(tags, list):
            tags = ','.join(tags)
        
        # Create new job
        new_job = Job(
            title=data['title'],
            company=data['company'],
            location=data['location'],
            posting_date=data.get('posting_date', 'Just posted'),
            job_type=data.get('job_type', 'Full-time'),
            tags=tags
        )
        
        db.session.add(new_job)
        db.session.commit()
        
        return jsonify({
            'message': 'Job created successfully',
            'job': new_job.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# READ Get all jobs with optional filtering and sorting
@job_bp.route('', methods=['GET'])
def get_jobs():
    try:
        query = Job.query
        
        # Filter by job_type
        job_type = request.args.get('job_type')
        if job_type:
            query = query.filter(Job.job_type == job_type)
        
        # Filter by location
        location = request.args.get('location')
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        
        # Filter by tag
        tag = request.args.get('tag')
        if tag:
            query = query.filter(Job.tags.ilike(f'%{tag}%'))
        
        # Search by keyword i.e title or company
        search = request.args.get('search')
        if search:
            query = query.filter(
                or_(
                    Job.title.ilike(f'%{search}%'),
                    Job.company.ilike(f'%{search}%')
                )
            )
        
        # Sorting
        sort = request.args.get('sort', 'posting_date_desc')
        if sort == 'posting_date_desc':
            query = query.order_by(desc(Job.created_at))
        elif sort == 'posting_date_asc':
            query = query.order_by(asc(Job.created_at))
        
        jobs = query.all()
        
        return jsonify({
            'count': len(jobs),
            'jobs': [job.to_dict() for job in jobs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ Get single job by ID
@job_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    try:
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(job.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE Update a job
@job_bp.route('/<int:job_id>', methods=['PUT', 'PATCH'])
def update_job(job_id):
    try:
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'title' in data:
            if not data['title']:
                return jsonify({'error': 'Title cannot be empty'}), 400
            job.title = data['title']
        
        if 'company' in data:
            if not data['company']:
                return jsonify({'error': 'Company cannot be empty'}), 400
            job.company = data['company']
        
        if 'location' in data:
            if not data['location']:
                return jsonify({'error': 'Location cannot be empty'}), 400
            job.location = data['location']
        
        if 'posting_date' in data:
            job.posting_date = data['posting_date']
        
        if 'job_type' in data:
            job.job_type = data['job_type']
        
        if 'tags' in data:
            tags = data['tags']
            if isinstance(tags, list):
                tags = ','.join(tags)
            job.tags = tags
        
        db.session.commit()
        
        return jsonify({
            'message': 'Job updated successfully',
            'job': job.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# DELETE Delete a job
@job_bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({'message': 'Job deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500