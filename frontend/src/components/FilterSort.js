import React, { useState } from 'react';
import './FilterSort.css';

const FilterSort = ({ onFilterChange, onReset }) => {
  const [filters, setFilters] = useState({
    search: '',
    job_type: '',
    location: '',
    tag: '',
    sort: 'posting_date_desc'
  });

  const [isExpanded, setIsExpanded] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    const newFilters = {
      ...filters,
      [name]: value
    };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleReset = () => {
    const resetFilters = {
      search: '',
      job_type: '',
      location: '',
      tag: '',
      sort: 'posting_date_desc'
    };
    setFilters(resetFilters);
    onReset();
  };

  const hasActiveFilters = filters.search || filters.job_type || filters.location || filters.tag;

  return (
    <div className="filter-sort-container">
      <div className="filter-header">
        <h2>Filter & Sort Jobs</h2>
        <button 
          className="toggle-filters-btn"
          onClick={() => setIsExpanded(!isExpanded)}
          aria-label={isExpanded ? 'Collapse filters' : 'Expand filters'}
        >
          {isExpanded ? '▲ Hide Filters' : '▼ Show Filters'}
        </button>
      </div>

      <div className={`filter-content ${isExpanded ? 'expanded' : ''}`}>
        {/* Search Bar */}
        <div className="filter-group full-width">
          <label htmlFor="search">
            🔍 Search by Title or Company
          </label>
          <input
            type="text"
            id="search"
            name="search"
            value={filters.search}
            onChange={handleChange}
            placeholder="e.g. Actuary, Pricing Analyst..."
            className="filter-input"
          />
        </div>

        <div className="filter-row">
          {/* Job Type Filter */}
          <div className="filter-group">
            <label htmlFor="job_type">
              💼 Job Type
            </label>
            <select
              id="job_type"
              name="job_type"
              value={filters.job_type}
              onChange={handleChange}
              className="filter-select"
            >
              <option value="">All Types</option>
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
              <option value="Internship">Internship</option>
            </select>
          </div>

          {/* Location Filter */}
          <div className="filter-group">
            <label htmlFor="location">
              📍 Location
            </label>
            <input
              type="text"
              id="location"
              name="location"
              value={filters.location}
              onChange={handleChange}
              placeholder="e.g. London, Remote..."
              className="filter-input"
            />
          </div>

          {/* Tag Filter */}
          <div className="filter-group">
            <label htmlFor="tag">
              🏷️ Tag/Keyword
            </label>
            <input
              type="text"
              id="tag"
              name="tag"
              value={filters.tag}
              onChange={handleChange}
              placeholder="e.g. Life, Health, Pricing..."
              className="filter-input"
            />
          </div>

          {/* Sort Options */}
          <div className="filter-group">
            <label htmlFor="sort">
              ⬆️ Sort By
            </label>
            <select
              id="sort"
              name="sort"
              value={filters.sort}
              onChange={handleChange}
              className="filter-select"
            >
              <option value="posting_date_desc">Date: Newest First</option>
              <option value="posting_date_asc">Date: Oldest First</option>
            </select>
          </div>
        </div>

        {/* Active Filters Summary */}
        {hasActiveFilters && (
          <div className="active-filters">
            <span className="active-filters-label">Active Filters:</span>
            <div className="filter-chips">
              {filters.search && (
                <span className="filter-chip">
                  Search: {filters.search}
                </span>
              )}
              {filters.job_type && (
                <span className="filter-chip">
                  Type: {filters.job_type}
                </span>
              )}
              {filters.location && (
                <span className="filter-chip">
                  Location: {filters.location}
                </span>
              )}
              {filters.tag && (
                <span className="filter-chip">
                  Tag: {filters.tag}
                </span>
              )}
            </div>
          </div>
        )}

        {/* Reset Button */}
        <div className="filter-actions">
          <button 
            className="reset-btn"
            onClick={handleReset}
            disabled={!hasActiveFilters}
          >
            🔄 Reset All Filters
          </button>
        </div>
      </div>
    </div>
  );
};

export default FilterSort;