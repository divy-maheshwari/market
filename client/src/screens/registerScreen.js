import React, { useState, useEffect } from 'react';
import {Link,useHistory} from 'react-router-dom';
import {useDispatch, useSelector} from 'react-redux'
import {register} from '../actions/userActions'

const Register = () => {
  const [name,setName] = useState('');
  const [email,setEmail] = useState('');
  const [isOwner,setIsOwner] = useState(false);
  const [password,setPassword] = useState('');
  const history = useHistory();
  const dispatch = useDispatch();
  const userRegister = useSelector(state => state.userRegister);
  const {loading,userInfo,error} = userRegister;

  useEffect(() => {
    if(userInfo) {
      history.push('/signIn');
    }
    else {
      history.push('/register')
    }
  },[userInfo]);
  
  const submitHandler = (e) => {
    e.preventDefault();
    dispatch(register(name,email,password,isOwner));
  }


    return (
        <div>
        {loading && <div>LOADING...</div>}
        {error && <div>{error}</div>}
        <form onSubmit={e => submitHandler(e)} style={{margin: "auto",width:"30%"}}>
             <div className="form-group ">
          <label htmlFor="exampleInputName">Name</label>
          <input type="text" name="name" className="form-control" id="exampleInputName" onChange={event => setName(event.target.value)} required/>
          </div>
        <div className="form-group ">
          <label htmlFor="exampleInputEmail1">Email address</label>
          <input type="email" className="form-control" name="email" id="exampleInputEmail1" onChange={event => setEmail(event.target.value)} aria-describedby="emailHelp" placeholder="example@gmail.com" required/>
          <small id="emailHelp" className="form-text text-muted">We'll never share your email with anyone else.</small>
        </div>
        <div className="form-group ">
          <label htmlFor="exampleInputPassword1">Password</label>
          <input type="password" className="form-control" name="password" onChange={event => setPassword(event.target.value)} id="exampleInputPassword1" required/>
        </div>
          <div className="custom-control custom-radio">
          <input type="radio" className="custom-control-input" onClick={() => {setIsOwner(true)}} id="defaultUnchecked" name="defaultExampleRadios"></input>
          <label className="custom-control-label" htmlFor="defaultUnchecked"><strong>Are you an Owner</strong></label>
        </div><br></br>
        <div className="form-group">
        <Link to="/signIn" >Already have an Account</Link>
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
        </form>
        </div>
    );
}

export default Register;