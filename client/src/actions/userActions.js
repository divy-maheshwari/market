import * as actions from '../constants'
import axios from 'axios'
import Cookie from 'js-cookie'

export const register = (name,email,password,isOwner) => (dispatch) => {
    dispatch({type:actions.REGISTER_REQUEST});
    axios.post('http://localhost:5000/api/user/register',{name,email,password,isOwner})
             .then(user => {
                 if(user.data.msg === "right"){
                 dispatch({type:actions.REGISTER_SUCCESS,payload:user.data});
                 Cookie.set('userInfo',JSON.stringify(user.data));
                 }
                 else {
                    dispatch({type:actions.REGISTER_FAILURE,payload:user.data.msg})
                 }
                })
             .catch(err => {
                 dispatch({type:actions.REGISTER_FAILURE,payload:err.message})
             });
}

export const signIn = (email,password) => (dispatch) => {
    let token = '';
    axios.post('http://localhost:5000/api/user/getToken',{email})
                             .then(data => {
                                token = data.data;
                             });
    dispatch({type:actions.SIGNIN_REQUEST});
    axios.post('http://localhost:5000/api/user/signIn',{email,password})
             .then(user => {
                 if(user.data.msg === " "){
                 dispatch({type:actions.SIGNIN_SUCCESS,payload:user.data});
                 Cookie.set('userInfo',JSON.stringify(user.data));
                 }
                 else {
                    dispatch({type:actions.SIGNIN_FAILURE,payload:user.data.msg});
                 }
             })
             .catch(err => {
                 dispatch({type:actions.SIGNIN_FAILURE,payload:err.message});
             });
}

