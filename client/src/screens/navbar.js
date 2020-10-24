import React from 'react'
import {Link} from 'react-router-dom'
import {useSelector} from 'react-redux'


const Navbar = () => {

  const userSignIn = useSelector(state => state.userSignIn);
  const {userInfo} = userSignIn;

        
    return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
    <Link className="navbar-brand" to="/">Market</Link>
    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span className="navbar-toggler-icon"></span>
    </button>
    <div className="collapse navbar-collapse" id="navbarSupportedContent">
      <ul className="navbar-nav ml-auto"> 
        <li className="nav-item">
        <Link className="nav-link" to="/products">edit-Product</Link>
        </li>
        <li className="nav-item">
        {userInfo ?  <Link className="nav-link" to="/profile">{userInfo.name}</Link> :
        <Link className="nav-link" to="/profile">profile</Link>}
        </li>
      </ul>
    </div>
  </nav>
  );
}


export default Navbar;