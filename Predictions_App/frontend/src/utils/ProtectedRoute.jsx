import { React, useContext} from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { AuthContext } from './store'


function ProtectedRoute() {
    //Set up constants

    const { authToken } = useContext(AuthContext)

    if (authToken) {
        console.log(authToken)
        return <Outlet />
        
    } else {
        console.log(authToken)
        console.log("No auth token recognized")
        return <Navigate to= "/login" />
    }
}
export default ProtectedRoute