import React, { useState, useEffect } from 'react';
import './App.css';
import JobList from './components/JobList';
import JobForm from './components/JobForm';
import FilterSort from './components/FilterSort';
import { getJobs, createJob, updateJob, deleteJob } from './api';

function App() {
  const [jobs, setJobs] = useState([]);
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [jobToEdit, setJobToEdit] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [currentFilters, setCurrentFilters] = useState({});

  // Fetch jobs on component mount
  useEffect(() => {
    fetchJobs();
  }, []);

  // Fetch jobs from API
  const fetchJobs = async (filters = {}) => {
    try {
      setLoading(true);
      setError(null);
      const response = await getJobs(filters);
      setJobs(response.jobs);
      setFilteredJobs(response.jobs);
    } catch (err) {
      setError(err.message || 'Failed to fetch jobs. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle filter changes
  const handleFilterChange = (filters) => {
    setCurrentFilters(filters);
    fetchJobs(filters);
  };

  // Reset filters
  const handleResetFilters = () => {
    setCurrentFilters({});
    fetchJobs();
  };

  // Show success message temporarily
  const showSuccessMessage = (message) => {
    setSuccessMessage(message);
    setTimeout(() => {
      setSuccessMessage('');
    }, 4000);
  };

  // Handle job creation
  const handleCreateJob = async (jobData) => {
    try {
      const response = await createJob(jobData);
      
      // Refresh job list with current filters
      await fetchJobs(currentFilters);
      
      setShowForm(false);
      showSuccessMessage('Job created successfully!');
    } catch (err) {
      throw new Error(err.message || 'Failed to create job');
    }
  };

  // Handle job update
  const handleUpdateJob = async (jobData) => {
    try {
      if (!jobToEdit) return;
      
      await updateJob(jobToEdit.id, jobData);
      
      // Refresh job list with current filters
      await fetchJobs(currentFilters);
      
      setJobToEdit(null);
      setShowForm(false);
      showSuccessMessage('Job updated successfully!');
    } catch (err) {
      throw new Error(err.message || 'Failed to update job');
    }
  };

  // Handle job deletion
  const handleDeleteJob = async (jobId) => {
    try {
      await deleteJob(jobId);
      
      // Refresh job list with current filters
      await fetchJobs(currentFilters);
      
      showSuccessMessage('Job deleted successfully!');
    } catch (err) {
      setError(err.message || 'Failed to delete job');
    }
  };

  // Handle edit button click
  const handleEditClick = (job) => {
    setJobToEdit(job);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Handle form submit
  const handleFormSubmit = (jobData) => {
    if (jobToEdit) {
      return handleUpdateJob(jobData);
    } else {
      return handleCreateJob(jobData);
    }
  };

  // Handle form cancel
  const handleFormCancel = () => {
    setShowForm(false);
    setJobToEdit(null);
  };

  // Handle add job button click
  const handleAddJobClick = () => {
    setJobToEdit(null);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="container">
          <h1>Job Listing Portal</h1>
          <p>Find your perfect actuarial career opportunity</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-content">
        {/* Success Message */}
        {successMessage && (
          <div className="success-message">
            <span>✓ {successMessage}</span>
            <button onClick={() => setSuccessMessage('')}>✕</button>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Add Job Button */}
        {!showForm && (
          <button 
            className="add-job-button"
            onClick={handleAddJobClick}
          >
            + Add New Job
          </button>
        )}

        {/* Job Form */}
        {showForm && (
          <JobForm
            jobToEdit={jobToEdit}
            onSubmit={handleFormSubmit}
            onCancel={handleFormCancel}
          />
        )}

        {/* Filter and Sort */}
        <FilterSort
          onFilterChange={handleFilterChange}
          onReset={handleResetFilters}
        />

        {/* Loading State */}
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p className="loading-text">Loading jobs...</p>
          </div>
        ) : (
          /* Job List */
          <JobList
            jobs={filteredJobs}
            onEdit={handleEditClick}
            onDelete={handleDeleteJob}
          />
        )}
      </main>
    </div>
  );
}

export default App;