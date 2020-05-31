// noprotect
var cols, rows;
var scl = 30;
var w = 1400;
var h = 1000;

var flying = 0;

var terrain = [];

function setup() {
  createCanvas(windowWidth, windowHeight, WEBGL);
  cols = w / scl;
  rows = h / scl;

  frameRate(60) ;
  
  
  noFill();
  smooth();
  stroke(183,0,255);
  for (var x = 0; x < cols; x++) {
    terrain[x] = [];
    for (var y = 0; y < rows; y++) {
      terrain[x][y] = 0;
    }
  }
  
}

function draw() {

  background(39,2,54);
  
  
  translate(0, 50);
  rotateX(PI / 3);
  translate(-w / 2, -h / 2);
  
  flying -= 0.001;
  var yoff = flying;
   let dirX = (mouseX / width - 0.5) * 2;
  let dirY = (mouseY / height - 0.5) * 2;
  directionalLight(250, 250, 250, -dirX, -dirY, -1);
  for (var y = 0; y < rows - 1; y++) {
    beginShape(TRIANGLE_STRIP);
    var xoff = 0;
    for (var x = 0; x < cols; x++) {
      terrain[x][y] = map(noise(xoff, yoff), 0, 1, 50, 300);
      xoff += 0.1;
      vertex(x * scl, y * scl, terrain[x][y]);
      vertex(x * scl, (y + 1) * scl, terrain[x][y + 1]);
    }
    yoff += 0.2;
    endShape();
  }

}

function mouseWheel(event) {
  flying += event.delta/100;
}