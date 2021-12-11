import { useState, useEffect } from 'react';
import fetchData from '../api/fetch_data';

import {
	DataGrid,
	GridToolbarContainer,
	GridToolbarExport,
	gridClasses,
} from '@mui/x-data-grid';
import _ from 'lodash';

const RushingRecordsTables = () => {
	const [playerRushingData, setPlayerRushingData] = useState();

	useEffect(async () => {
		const { data } = await fetchData();
		setPlayerRushingData(data);
	}, []);

	const customToolbar = () => {
		return (
			<GridToolbarContainer className={gridClasses.toolbarContainer}>
				<GridToolbarExport />
			</GridToolbarContainer>
		);
	};

	const columnNames = playerRushingData && _.keys(playerRushingData[0]);

	const createColumnNames = () => {
		return columnNames.map((key) => {
			const columnName = _.startCase(key);
			return { field: key, headerName: columnName, width: 150 };
		});
	};

	return (
		<div style={{ height: 1000, width: '100%' }}>
			{playerRushingData && customToolbar ? (
				<DataGrid
					rows={playerRushingData}
					columns={createColumnNames()}
					components={{
						Toolbar: customToolbar,
					}}
				/>
			) : (
				<></>
			)}
		</div>
	);
};

export default RushingRecordsTables;
