let ssize = 5; 
let dim;

function setup() {
  frameRate(60);
	createCanvas(windowWidth, windowHeight);
  colorMode(HSB, 360, 100, 100);
  ellipseMode(RADIUS);
  noStroke(); 
}

function draw() {
	background(0); 
  for(let x = 0 ; x < windowWidth ; x += ssize+10 ) {
    for ( let y = 0 ; y < windowHeight; y += ssize+10 ) {
      fill((dist(x,y,windowWidth/2,windowHeight/2)+(frameCount/5))%255, 90, 90);
      circle(x,y,sin(((dist(x,y,windowWidth/2,windowHeight/2)/10)+frameCount/10))*(frameCount/300));
    }
  }
}

