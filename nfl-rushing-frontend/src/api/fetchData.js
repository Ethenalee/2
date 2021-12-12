import axios from 'axios';
import { RUSHING_URL } from '../constants/url';

const fetchData = async (params) => {
	return axios
		.get(RUSHING_URL)
		.then((res) => res.data)
		.catch((err) => err);
};

export default fetchData;
