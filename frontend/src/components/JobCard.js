import React from 'react';
import './JobCard.css';

const JobCard = ({ job, onEdit, onDelete }) => {
  const handleDelete = () => {
    const confirmed = window.confirm(
      `Are you sure you want to delete the job "${job.title}" at ${job.company}?`
    );
    
    if (confirmed) {
      onDelete(job.id);
    }
  };

  return (
    <div className="job-card">
      <div className="job-card-header">
        <h3 className="job-title">{job.title}</h3>
        <span className="job-type-badge">{job.job_type}</span>
      </div>
      
      <div className="job-card-body">
        <div className="job-info">
          <span className="job-company">
            <i className="icon">🏢</i>
            {job.company}
          </span>
          <span className="job-location">
            <i className="icon">📍</i>
            {job.location}
          </span>
          <span className="job-date">
            <i className="icon">📅</i>
            {job.posting_date}
          </span>
        </div>
        
        {job.tags && job.tags.length > 0 && (
          <div className="job-tags">
            {job.tags.map((tag, index) => (
              <span key={index} className="job-tag">
                {tag.trim()}
              </span>
            ))}
          </div>
        )}
      </div>
      
      <div className="job-card-footer">
        <button 
          className="btn btn-edit"
          onClick={() => onEdit(job)}
          aria-label="Edit job"
        >
          ✏️ Edit
        </button>
        <button 
          className="btn btn-delete"
          onClick={handleDelete}
          aria-label="Delete job"
        >
          🗑️ Delete
        </button>
      </div>
    </div>
  );
};

export default JobCard;