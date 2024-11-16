import {GraphQLClient} from "graphql-request"

const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/graphql"
export const gqlClient = new GraphQLClient(apiUrl)
