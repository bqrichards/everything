import axios from 'axios'

export const BASE_URL = 'http://127.0.0.1:5000/api'

export const urlFromEndpoint = (endpoint: string) => `${BASE_URL}/${endpoint}`

export const api = axios.create({
	baseURL: BASE_URL
})
