import mockedAxios from 'axios';
import { cleanup } from '@testing-library/react';

import { RUSHING_URL } from '../../constants/url';
import fetchData from '../../api/fetchData';
import testData from './testData';

jest.mock('axios');
afterEach(cleanup);

test('axios been called', async () => {
	mockedAxios.get.mockResolvedValueOnce(testData);
	const data = await fetchData();
	expect(mockedAxios.get).toHaveBeenCalledWith(RUSHING_URL);
	expect(data).toBe(testData['data']);
});
