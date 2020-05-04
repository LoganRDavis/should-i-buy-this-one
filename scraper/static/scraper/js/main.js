'use strict';

$(document).ready(function () {
    $('#searchSubmit').on('click', () => {
        fetch('/', {
            method: 'post',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: $('#searchName').val(), 
                priceWeight: $('#searchPriceWeight').val(), 
                ratingWeight: $('#searchRatingWeight').val(), 
                reviewCountWeight: $('#searchReviewCountWeight').val(), 
            })
        }).then((res) => {
            if (!res.ok) { throw res; }
            return res.json();
        }).then((resJson) => {
            showResults(resJson)
        }).catch((err) => {
            try {
                err.text().then((text) => {
                    console.log(text);
                })
            } catch (err2) {
                console.log(err);
            }
        });   
    })
});

function showResults(resJson) {
    let topResult = resJson[resJson.length - 1];
    let htmlContent = 
        `<h2>Top Result:</h2>
        <a href="${topResult.url}">
            <img src="${topResult.imageUrl}">
            <h3>${topResult.title}</h3>
            <p>$${topResult.price} from ${topResult.store}<br>
            Reviews: ${topResult.rating} of 5 (${topResult.reviewCount})</p>
        </a>`;
    $('#mainContent').html(htmlContent);

    let moreResults = '<hr><h2>More Results:</h2>'
    for (let result of resJson) {
        if (result === topResult) {
            continue;
        }
        moreResults += 
        `<a href="${result.url}">
            <img src="${result.imageUrl}">
            <h3>${result.title}</h3>
            <p>$${result.price} from ${result.store}<br>
            Reviews: ${result.rating} of 5 (${result.reviewCount})</p>
        </a>`;
    }
    $('#moreResults').html(moreResults).show();
}