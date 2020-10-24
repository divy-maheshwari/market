const express = require('express')
const router = express.Router();
const isAuth = require('../config/jwt').isAuth;
const Product = require('../models/productModel');
const nodemailer = require('nodemailer');
const sendGridTransport = require('nodemailer-sendgrid-transport');
const apiKey = require('../config/keys').SEND_GRID_KEY;


router.get('/',(req,res) => {
    Product.find({},(err,products) => {
        if(products) {
            res.json(products);
        }
        else {
            res.json([]);
        }
    });
});


router.post('/',isAuth,(req,res) => {
    const transporter = nodemailer.createTransport(
        sendGridTransport({
            auth: {
              api_key: apiKey,
            },
          })
    );
    let mailOptions = {
        from: `${req.user.email}`,
        to: "divym07@gmail.com",
        subject: "Adding new product",
        text: "That was easy!",
        html: "<div style =" +
          "width:100%; height:100%;  " +
          "><h1 style=" +
          "font-weight:500>Hey, Admin " +
          "</h1> <br><h1>" + `${req.user.name}`+ " added a new product named " + `${req.body.name} `+"</h1></div><p>If this information is unknown please kindly ignore this mail.</p><p>Regards, <strong>Market</strong></p>",

      };
      transporter.sendMail(mailOptions,(err,info) => {
          if(err) {
              console.log(err);
          }
          else {
            const product = new Product({
                name:req.body.name,
                price:req.body.price,
                description:req.body.description,
                countInStock:req.body.countInStock,
                image:req.body.image
            });
            product.save()
                        .then(productData => {
                            res.json(productData);
                        });
          }
      });
});


router.put('/:id',isAuth,(req,res) => {
    const transporter = nodemailer.createTransport(
        sendGridTransport({
            auth: {
              api_key: apiKey,
            },
          })
    );
    let mailOptions = {
        from: `${req.user.email}`,
        to: "divym07@gmail.com",
        subject: "Updating product",
        text: "That was easy!",
        html: "<div style =" +
          "width:100%; height:100%;  " +
          "><h1 style=" +
          "font-weight:500>Hey, Admin " +
          "</h1> <br><h1>" + `${req.user.name}`+ " made some changes to product named " + `${req.body.name} `+"</h1></div><p>If this information is unknown please kindly ignore this mail.</p><p>Regards, <strong>Market</strong></p>",
      };
      transporter.sendMail(mailOptions,(err,info) => {
          if(err) {
              console.log(err);
          }
          else {
            Product.findByIdAndUpdate(req.params.id,req.body,(err,updatedProduct) => {
                if(err) {
                    res.json({msg: 'failed to update the product'})
                }
                else {
                    updatedProduct.save()
                    .then(product => {
                        res.json(product)
                    })
                }
            });
          }
      });
});

router.delete('/:id',isAuth,(req,res) => {
    const transporter = nodemailer.createTransport(
        sendGridTransport({
            auth: {
              api_key: apiKey,
            },
          })
    );
    let mailOptions = {
        from: `${req.body.email}`,
        to: "divym07@gmail.com",
        subject: "Deleting Product",
        text: "That was easy!",
        html: "<div style =" +
          "width:100%; height:100%;  " +
          "><h1 style=" +
          "font-weight:500>Hey,  Admin " +
          "</h1> <br><h1>" + `${req.user.name}`+ " deleted a product named " + `${req.body.name} `+"</h1></div><p>If this information is unknown please kindly ignore this mail.</p><p>Regards, <strong>Market</strong></p>",

      };
      transporter.sendMail(mailOptions,(err,info) => {
          if(err) {
              console.log(err);
          }
          else {
            Product.findByIdAndDelete(req.params.id,req.body,(err,deletedProduct) => {
                if(deletedProduct) {
                    res.json({msg: 'product deleted'});
                }
                else {
                    res.json({msg: 'product failed to delete'})
                }
            });
          }
      });
});


router.post('/upload',(req,res) => {
    if(req.files) {
        const file = req.files.image;
        file.mv(`C:/Users/divy maheshwari/MernProjects/Restaurant/client/public/uploads/${file.name}`,err => {
            if(err) {
               return res.status(500).json(err);
            }
            res.json(file.name);
        });
    }
    else {
        return res.status(500).json({msg:'no file uploaded'});
    }
});

module.exports = router;