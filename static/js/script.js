function runNewAnalysis() {
    // Show modal
    document.getElementById('loading-modal').style.display = "flex";

    // Simulate async operation
    setTimeout(function() {
        // Update the container with new Analysis
        fetchNewAnalysisResults();
        
        // Hide loading modal when the new analysis is complete
        setTimeout(function() {
            document.getElementById('loading-modal').style.display = "none";
        }, 2000);
    }, 1000);       // 2000 millisecond = 2 sec
}


function fetchNewAnalysisResults() {
    // Use AJAX or fetch to get new analysis using url Route
    fetch('/get_new_analysis')
        .then(response => response.json())
        .then(data => {
            // Update tweet container
            updateTweetContainerWithNewAnalysis(data);
        })
        .catch(error => {
            console.error("Error fetching new analysis results: ", error);
        });
}


function toggleNav() {
    var navLinks = document.querySelector('.burger-nav-links');
    navLinks.classList.toggle('show');
    
    var x = document.querySelector('.burger');
    x.classList.toggle('change');
}


function closeBurgerNavIfExceedsWith() {
    var navLinks = document.querySelector('.burger-nav-links');
    var x = document.querySelector('.burger');

    // Check the window size
    if (window.innerWidth > 768) {
        // Close navigation if it is open
        if (navLinks.classList.contains('show')) {
            navLinks.classList.remove('show');
            x.classList.remove('change');
        }
    }
}


// Add event listeners
window.addEventListener('resize', closeBurgerNavIfExceedsWith);

// Call closeNavIfExceedsWidth on page load
window.addEventListener('load', closeBurgerNavIfExceedsWith);


function createEmojiSVG(filename) {
    const svg = document.createElement('img');
    svg.src = `static/images/${filename}`;
    return svg;
}


function updateTweetContainerWithNewAnalysis(newAnalysisResults) {
    // Clear existing content and reset to top
    document.getElementById('tweet-container').innerHTML = '';
    document.getElementById('tweet-container').scrollTop = 0;

    // Loop through new analysis results and update tweet-container
    newAnalysisResults.forEach(tweet_structure => {
        const tweetContainer = document.getElementById('tweet-container');
        tweetContainer.className = "tweet-container";

        // Creat new tweet structure elements
        const tweetDiv = document.createElement('div');
        tweetDiv.className = "item item-1";

        const username = document.createElement('h3');
        username.textContent = `@${tweet_structure.username}`;

        const tweet = document.createElement('p');
        tweet.textContent = tweet_structure.tweet;

        // Create SVG elements for emojis from file directory
        const positiveEmoji = createEmojiSVG('positive.svg');
        const neutralEmoji = createEmojiSVG('neutral.svg');
        const negativeEmoji = createEmojiSVG('negative.svg');

        // Create the overall sentimentAnalysis container
        const sentimentAnalysis = document.createElement('p');
        sentimentAnalysis.className = "sentiment";

        // Create elements for positive sentiment
        const positiveSpan = document.createElement('span');
        const positiveImage = createEmojiSVG('positive.svg');
        positiveSpan.appendChild(positiveImage);
        const positiveText = document.createTextNode(` ${tweet_structure.analysis.Positive}%`);
        positiveSpan.appendChild(positiveText);

        // Append positive elements to sentimentAnalysis container
        sentimentAnalysis.appendChild(positiveSpan);

        // Create elements for neutral sentiment
        const neutralSpan = document.createElement('span');
        const neutralImage = createEmojiSVG('neutral.svg');
        neutralSpan.appendChild(neutralImage);
        const neutralText = document.createTextNode(` ${tweet_structure.analysis.Neutral}%`);
        neutralSpan.appendChild(neutralText);

        // Append neutral elements to sentimentAnalysis container
        sentimentAnalysis.appendChild(neutralSpan);

        // Create elements for negative sentiment
        const negativeSpan = document.createElement('span');
        const negativeImage = createEmojiSVG('negative.svg');
        negativeSpan.appendChild(negativeImage);
        const negativeText = document.createTextNode(` ${tweet_structure.analysis.Negative}%`);
        negativeSpan.appendChild(negativeText);

        // Append negative elements to sentimentAnalysis container
        sentimentAnalysis.appendChild(negativeSpan);

        
        // Append elements to tweetDiv
        tweetDiv.appendChild(username);
        tweetDiv.appendChild(tweet);
        tweetDiv.appendChild(sentimentAnalysis);

        // Append tweetDiv to tweet-container
        tweetContainer.appendChild(tweetDiv);
    })
}



// Responsive Header
function toggleNav() {
    var navLinks = document.querySelector('.burger-nav-links');
    navLinks.classList.toggle('show');
    
    var x = document.querySelector('.burger');
    x.classList.toggle('change');
}


function closeBurgerNavIfExceedsWith() {
    var navLinks = document.querySelector('.burger-nav-links');
    var x = document.querySelector('.burger');

    // Check the window size
    if (window.innerWidth > 768) {
        // Close navigation if it is open
        if (navLinks.classList.contains('show')) {
            navLinks.classList.remove('show');
            x.classList.remove('change');
        }
    }
}


// Add event listeners
window.addEventListener('resize', closeBurgerNavIfExceedsWith);

// Call closeNavIfExceedsWidth on page load
window.addEventListener('load', closeBurgerNavIfExceedsWith);
