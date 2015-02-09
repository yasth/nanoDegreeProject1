import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="http://cdn.jsdelivr.net/qtip2/2.2.1/jquery.qtip.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="http://cdn.jsdelivr.net/qtip2/2.2.1/jquery.qtip.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
            vertical-align:bottom;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
           $('.hasTooltip').each(function() { // Notice the .each() loop, discussed below
           $(this).qtip({ //adds on tooltip for each movie
            content: {
                text: $(this).data("copy")
            },position: {
        target: 'mouse', // Position it where the click was...
        adjust: { mouse: false } // ...but don't follow the mouse
    }
           });
         });
        });
       
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="hasTooltip col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer" data-copy="{copy}">
    <img src="{poster_image_url}" width="220" height="342">
    <h2>{movie_title}</h2>
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            copy = movie.copy
        )
    return content

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible

class Movie:
    """Movie class is used to define the several aspects that define a movie trailer
        title-Tile of movie
        poster_image_url - http image path
        trailer_youtube_url - http of youtube video
        copy -- a bit of copy to be thrown in a tool tip


    """ 
    
    def __init__(self,title,poster_image_url,trailer_youtube_url,copy):
        self.title=title
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url
        self.copy = copy



movies = [Movie('Black Snake Moan', 'http://ia.media-imdb.com/images/M/MV5BNzE4NzY0NzM2MF5BMl5BanBnXkFtZTcwMTc4MTY0MQ@@._V1_SY317_CR0,0,214,317_AL_.jpg','https://www.youtube.com/watch?v=VYMqX3SKIGY','A love story'),
          Movie('Anaconda', 'http://ia.media-imdb.com/images/M/MV5BMTMzMTU5NjcxNl5BMl5BanBnXkFtZTcwMzE2NDU2MQ@@._V1_SX214_AL_.jpg','https://www.youtube.com/watch?v=zkX5t5ZJLEk','A happy movie about scientific research'),
          Movie('The Holy Grail ', 'http://ia.media-imdb.com/images/M/MV5BMTkzODczMTgwM15BMl5BanBnXkFtZTYwNTAwODI5._V1_SX214_AL_.jpg','https://www.youtube.com/watch?v=RDM75-oXGmQ','An unbiased documentary about the french '),
          Movie('Snakes On a Plane', 'http://ia.media-imdb.com/images/M/MV5BMjE0NzI3MjkxM15BMl5BanBnXkFtZTcwNjEzODIzMQ@@._V1_.jpg','https://www.youtube.com/watch?v=u6Squ9a2kO4','A movie about transporting snakes ')]

def main():
    open_movies_page(movies)

if __name__ == "__main__":
    main()
