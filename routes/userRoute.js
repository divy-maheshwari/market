const express = require('express')
const router = express.Router();
const bcrypt = require('bcryptjs');
const User = require('../models/userModel');
const getToken = require('../config/jwt').getToken;
const bcryptjs = require('bcryptjs');


router.post('/register',(req,res) => {
    const {name,email,password,isOwner} = req.body;
    User.findOne({email},(err,user) => {
        if(user) {
            res.json('user already registered');
        }
        else {
            const user = new User({name,email,password,isOwner});
                bcrypt.genSalt(10,(err,salt) => {
                    bcrypt.hash(user.password,salt,(err,hash) => {
                        if(err) {throw err;}
                        else{
                        user.password = hash;
                        user.save()
                          .then(userData => {
                              userData.token = getToken(userData);
                              User.findByIdAndUpdate(userData._id,userData,(err,updatedUserData) => {
                                  if(updatedUserData){
                                      updatedUserData.save()
                                      .then(information => {
                                        res.json({
                                            name:information.name,
                                            email:information.email,
                                            _id:information._id,
                                            token:getToken(information),
                                            isAdmin:information.isAdmin,
                                            isOwner:information.isOwner,
                                            msg:"right"
                                        });
                                      });
                            }
                              })
                          });
                        }
                    })
                });
        }      
   })
});


router.post('/signIn',(req,res) => {    
    const {email,password} = req.body;
    User.findOne({email},(err,user) => {
        if(user) {
                bcryptjs.compare(password,user.password,(err,ismatch) => {
                    if(err){
                        res.json({msg:"password is incorrect"});
                    }
                    if(ismatch){
                        res.json({name:user.name,
                            email:user.email,
                            _id:user._id,
                            isAdmin:user.isAdmin,
                            token:getToken(user),
                            isOwner:user.isOwner,
                            msg: " "  
                        });
                    }
                })
        }
    }); 
});




router.post('/getToken',(req,res) => {
    User.findOne({email:req.body.email},(err,user) => {
        if(err) {
           res.json("noToken");
        }
        else {
            res.json(user.token);
        }
    })
});




router.get('/createAdmin',(req,res) =>{
    const userData = new User({
        name: 'divy',
        email: 'divym07@gmail.com',
        password: '12345',
        isAdmin: true,
        isOwner: false
    })
    userData.save()
              .then(user => {
                user.token = getToken(user);
                User.findByIdAndUpdate(user._id,user,(err,updatedUserData) => {
                    if(updatedUserData){
                        updatedUserData.save()
                        .then(information => {
                          res.json({
                              name:information.name,
                              email:information.email,
                              _id:information._id,
                              token:getToken(information),
                              isAdmin:information.isAdmin,
                              isOwner:information.isOwner
                          });
                        });
              }
                })
            });
        });


module.exports = router;