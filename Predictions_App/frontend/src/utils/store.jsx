//Imports
import React from 'react'

export const AuthContext = React.createContext(null)

export default ({children}) => {

    const [authToken, setAuthToken] = React.useState(null)

    const store = {
        authToken, 
        setAuthToken
    }

    return <AuthContext.Provider value={store}>{children}</AuthContext.Provider>
}