import { useState, useEffect } from 'react';
import fetchData from '../api/fetch_data';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TablePagination from '@mui/material/TablePagination';
import Paper from '@mui/material/Paper';
import { CSVLink, CSVDownload } from "react-csv";
import _ from "lodash";

const RushingTables = () => {
	const [playerRushingData, setPlayerRushingData] = useState();
  const [playerRushingMetaData, setPlayerRushingMetaData] = useState();

	useEffect(async () => {
		const { data, meta } = await fetchData();
		setPlayerRushingData(data);
    setPlayerRushingMetaData(meta);
	}, []);

  // Todo add filter, sorting features
  const columnNames = playerRushingData && _.keys(playerRushingData[0])

	const createColumnNames = () => {
		return columnNames.map((key, i) => {
      const columnName = _.startCase(key)
			return (
				<TableCell onClick={() => key === 'name' && sortByName()} key={i} align='right'>
					{columnName}
				</TableCell>
			);
		});
	};

	const createTableRows = () => {
		return playerRushingData.map((row) =>
			<TableRow
				key={row.name}
			>
				{columnNames.map((key, i) =>
					<TableCell key={i} align='right'>
						{row[key]}
					</TableCell>
				)}
			</TableRow>
		);
	};

	return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
		<TableContainer component={Paper}>
			{playerRushingData &&  playerRushingMetaData ? (
        <>
        <CSVLink data={playerRushingData}>Download CSV</CSVLink>
				<Table stickyHeader sx={{ minWidth: 650 }} aria-label='sticky table'>
					<TableHead>
          <TableRow>Total Result: {playerRushingMetaData["total_results"]}</TableRow>
						<TableRow>{columnNames && createColumnNames()}</TableRow>
					</TableHead>
					<TableBody>
						{createTableRows()}
					</TableBody>
				</Table>
        </>
			) : (
				<></>
			)}
		</TableContainer>
    </Paper>
	);
};

export default RushingTables;
