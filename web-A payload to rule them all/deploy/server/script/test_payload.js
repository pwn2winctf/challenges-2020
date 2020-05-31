#!/usr/bin/env node

const puppeteer = require('puppeteer')
const mysql = require("mysql")
const util = require('util')
const libxml = require("libxmljs")
const fs = require("fs")
const sanitizeHtml = require("sanitize-html")



function test_xxe(payload) {

	try {
		var my_secret = Math.random().toString(36).substring(2) ;
		fs.writeFileSync("/home/gnx/script/xxe_secret",my_secret)
		var doc = libxml.parseXml(payload, { noent: true ,nonet: true })
		return doc.toString().includes(my_secret) 
		
	} catch (e) {
		return false
	}
} 

async function test_xss(payload) {
	try {
		const browser = await puppeteer.launch({args:['--no-sandbox', '--disable-setuid-sandbox','--disable-dev-shm-usage','--disable-accelerated-2d-canvas','--no-first-run','--no-zygote','--single-process','--disable-gpu']})
		const page = await browser.newPage()
		page.setDefaultNavigationTimeout(1000);
		payload = sanitizeHtml(payload,{allowedTags:[]})
		await page.goto(`data:text/html,<script>${payload}</script>`)
		const check = await page.evaluate("( typeof xss != 'undefined' ? true : false )") // vlw herrera

		await browser.close()
		
		return check

	} catch (error) {
		console.error(error)
	}

}

async function test_sqli(payload) {

	var connection = mysql.createConnection({
		host : process.env.MYSQL_HOST || "127.0.0.1",
		user : process.env.MYSQL_USER,
		password : process.env.MYSQL_PASSWORD,
		database : process.env.MYSQL_DATABASE,
		charset: 'utf8',
    dialectOptions: {
			collate: 'utf8_general_ci',
    },
	})


	const query = util.promisify(connection.query).bind(connection)


	connection.connect()

	const users = await query("SELECT * from users") 
	try {
		const sqli = await query(`SELECT * from posts where id='${payload}'`)
		await connection.end() 
		return JSON.stringify(sqli).includes(users[0]["password"])	
	} catch(e) {
		return false
	}
}

function main(args){

	var xss = test_xss(args[0])
	var sqli = test_sqli(args[0])
	var xxe = test_xxe(args[0])

  Promise.all([xss,sqli]).then( function( values ){
                if ( values[0] && values[1] && xxe ) {
                        console.log("parabens hackudo")
                } else {
                        console.log("hack harder")
                }

                process.exit(0)
        })
	
}

main(process.argv.slice(2))
