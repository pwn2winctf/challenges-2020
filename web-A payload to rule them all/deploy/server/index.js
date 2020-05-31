const express = require("express")
const app = express()
const bodyParser = require("body-parser")
const port = 31337
const { execFile } = require("child_process")
const fs = require("fs")

app.use(express.static("static"))
app.use(bodyParser.urlencoded({extended:true}))

app.post('/', (req,res) => {
	const test_payload = execFile("/usr/sbin/gosu",["gnx","/home/gnx/script/test_payload.js",req.body.payload], ( error, stdout, stderr ) => {
	if ( stdout.toString().trim() === "parabens hackudo" ) {
			res.send(process.env.FLAG)
		} else {
			res.send("nope")
		}
	});
	console.log(req.body.payload)

})


app.get('/source', (req,res) => {
	var out = "/usr/src/app/index.js :\n\n" + fs.readFileSync("/usr/src/app/index.js").toString() + "\n\n"
	out += "/home/gnx/script/test_payload.js :\n\n" + fs.readFileSync("/home/gnx/script/test_payload.js") + "\n\n"
	res.send(out)
})

app.listen(port,'0.0.0.0', () => console.log(`Chall rodando em http://localhost:${port}`))
