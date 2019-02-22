import React from 'react'
import PropTypes from 'prop-types'

import './styles.scss';

const Review = ({ review }) => {
    const { reviewUrl, author, score, recommendation } = review

    return (
        <li className="reviews-sidebar__item">
            <a target="_blank" rel="noopener noreferrer" href={reviewUrl}>{author}</a>
            <div>{recommendation.display}</div>
            <div>{score}</div>
        </li>
    )
}

Review.propTypes = {
    review: PropTypes.shape({
        author: PropTypes.string.isRequired,
        score: PropTypes.number.isRequired,
        recommendation: PropTypes.shape({
            display: PropTypes.string.isRequired,
        }).isRequired,
        reviewUrl: PropTypes.string.isRequired,
    }),
}

const ReviewBlock = ({ review }) => {
    const renderReviews = () => {
        if (review.reviews.length === 0) {
            return <p>No reviews found.</p>
        }

        return review.reviews.map(review =>
            <Review key={review.id} {...{ review }} />)
    }

    const renderTrafficLight = () => {
        const verdict = review.recommendation.display;
        const letter = verdict.charAt(0)

        let modifierClass;
        if (verdict === 'No') {
            modifierClass = 'red'
        } else if (verdict === 'Yes') {
            modifierClass = 'green'
        } else if (verdict === 'Maybe') {
            modifierClass = 'amber'
        }

        return <div aria-label="Traffic light score" className={`traffic-light traffic-light--${modifierClass}`}>{letter}</div>
    }

    const renderReviewBody = () => {
        if (review === undefined) {
            return null
        }

        return (
            <ul className="reviews-sidebar">
                {review.recommendation.display &&
                    <li className="reviews-sidebar__item reviews-sidebar__item--header">
                        <div></div>
                        {review.recommendation.display &&
                            renderTrafficLight()
                        }
                        {!isNaN(parseFloat(review.score)) &&
                            <div>{review.score}</div>
                        }
                    </li>
                }
                {renderReviews()}
            </ul>
        )
    }

    return (
        <div className="review-block">
            <h5>Reviews &amp; assignees</h5>
            {renderReviewBody()}
        </div>
    )
}

ReviewBlock.propTypes = {
    review: PropTypes.shape({
        score: PropTypes.number,
        recommendation: PropTypes.shape({
            display: PropTypes.string,
        }),
        reviews: PropTypes.arrayOf(PropTypes.shape({
            id: PropTypes.number,
        })),
    }),
}

export default ReviewBlock