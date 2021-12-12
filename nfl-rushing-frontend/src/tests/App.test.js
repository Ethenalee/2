import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders App loading table component', () => {
  render(<App />);
  const linkElement = screen.getByTestId('rushingrecords-tables');
  expect(linkElement).toBeInTheDocument();
});
