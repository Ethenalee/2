import { render, screen, cleanup, waitForElement } from '@testing-library/react';
import { waitFor } from '@testing-library/dom';

import mockedAxios from 'axios';

import { RUSHING_URL } from '../../constants/url';
import testData from '../api/testData';
import RushingRecordsTables from '../../components/RushingRecordsTables';

jest.mock('axios');
afterEach(() => cleanup)

test('render RushingRecordsTables call axios', async () => {
	mockedAxios.get.mockResolvedValueOnce(testData);
	render(<RushingRecordsTables />);
	expect(mockedAxios.get).toHaveBeenCalledWith(RUSHING_URL);
	expect(mockedAxios.get).toHaveBeenCalledTimes(1);

});

test('render RushingRecordsTables load a table', async () => {
	mockedAxios.get.mockResolvedValueOnce(testData);
	render(<RushingRecordsTables />);

	await waitFor(() => expect(mockedAxios.get).toHaveBeenCalledTimes(1),
	expect(screen.findByTestId('rushingrecords-data-grid')).not.toBeNull())
});

test('render RushingRecordsTables when waiting for loadind data do not have a table', () => {
	mockedAxios.get.mockResolvedValueOnce(testData);
	render(<RushingRecordsTables />);

	expect(screen.queryByTestId('rushingrecords-data-grid')).toBeNull();
});
