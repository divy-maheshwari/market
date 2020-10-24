import React from 'react';
import {BrowserRouter as Router,Switch,Route} from 'react-router-dom'
import Navbar from './screens/navbar';
import HomeScreen from './screens/homescreen'
import Register from './screens/registerScreen'
import LogIn from './screens/loginScreen'
import Profile from './screens/profileScreen'
import ProductScreen from './screens/productScreen'

const  App = () => {
    return (

        <Router>
            <Navbar />
            <Switch>
                <Route path="/" exact component={HomeScreen} />
                <Route path="/register" component={Register} />
                <Route path="/signIn" component={LogIn} />
                <Route path="/products" component={ProductScreen} />
                <Route path="/profile" component={Profile} />
            </Switch>
        </Router>
    )

}

export default App;