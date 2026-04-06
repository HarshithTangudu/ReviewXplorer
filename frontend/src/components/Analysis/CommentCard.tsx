import React from 'react';
import { CommentResult } from '../../types';

interface CommentCardProps {
  comment: CommentResult;
}

const CommentCard: React.FC<CommentCardProps> = ({ comment }) => {
  return (
    <div className="comment-card glow-card">
      <p className="comment-text">{comment.text}</p>
      <div className="badges">
        <span className={`badge badge-${comment.sentiment.toLowerCase()}`}>{comment.sentiment}</span>
        <span className="badge badge-emotion">{comment.emotion}</span>
        {comment.sarcastic && <span className="badge badge-sarcasm">Sarcastic</span>}
      </div>
    </div>
  );
};

export default CommentCard;
