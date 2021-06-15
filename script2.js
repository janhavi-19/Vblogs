const sliders = document.querySelector(".carouselbox");

var scrollPerClick=1200;

var ImagePadding = 20;



showMovieData();



var scrollamount=0;

function sliderScrollLeft(){

    sliders.scrollTo({

        top:0,

        left: (scrollamount -= scrollPerClick),

        behavior: "smooth"

    });

    if(scrollamount<0)

    {

        scrollamount=0;

    }

}

function sliderScrollRight() {

    if(scrollamount<= sliders.scrollWidth - sliders.clientWidth){

        sliders.scrollTo({

            top:0,

            left: (scrollamount+=scrollPerClick),

            behavior: "smooth"

        })

    }

}









async function showMovieData() {

  const api_key = "742286bb455829ac74ab65e30edb9982";



  var result = await axios.get(

    "https://api.themoviedb.org/3/discover/movie?api_key=" +

      api_key +

      "&sort_by=popularity.desc"

  );x

  console.log(result);

  result = result.data.results;

  result.map(function (cur, index) {

    sliders.insertAdjacentHTML(

      "beforeend",

      `<img class="img-${index} slider-img" src="https://image.tmdb.org/t/p/w185/${cur.poster_path}" />`

    );

  });



  // scrollPerClick = 400;

}
