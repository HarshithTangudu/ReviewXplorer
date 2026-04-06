import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { CommentResult } from '../../types';
import CommentCard from './CommentCard';

interface CommentListProps {
  comments: CommentResult[];
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

const CommentList: React.FC<CommentListProps> = ({ comments, currentPage, totalPages, onPageChange }) => {
  return (
    <div className="comment-list">
      <div className="list-header">
        <h3>Analyzed Reviews</h3>
        <div className="pagination">
          <button 
            onClick={() => onPageChange(Math.max(1, currentPage - 1))} 
            disabled={currentPage === 1}
          >
            <ChevronLeft size={20} />
          </button>
          <span className="page-info">Page {currentPage} of {totalPages}</span>
          <button 
            onClick={() => onPageChange(Math.min(totalPages, currentPage + 1))} 
            disabled={currentPage === totalPages}
          >
            <ChevronRight size={20} />
          </button>
        </div>
      </div>
      {comments.map((res, idx) => (
        <CommentCard key={idx} comment={res} />
      ))}
    </div>
  );
};

export default CommentList;
