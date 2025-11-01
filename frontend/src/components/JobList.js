import React from 'react';
import JobCard from './JobCard';
import './JobList.css';

const JobList = ({ jobs, onEdit, onDelete }) => {
  if (!jobs || jobs.length === 0) {
    return (
      <div className="no-jobs">
        <h3>No jobs found</h3>
        <p>Try adjusting your filters or add a new job to get started.</p>
      </div>
    );
  }

  return (
    <div className="job-list-container">
      <div className="job-count">
        <strong>{jobs.length}</strong> {jobs.length === 1 ? 'job' : 'jobs'} found
      </div>
      <div className="job-list">
        {jobs.map((job) => (
          <JobCard 
            key={job.id} 
            job={job} 
            onEdit={onEdit}
            onDelete={onDelete}
          />
        ))}
      </div>
    </div>
  );
};

export default JobList;