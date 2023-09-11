import React, { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import { styled, useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import CircularProgress from '@mui/material/CircularProgress';

const StyledContainer = styled(Container)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
`;

const App = () => {
  const [inputValue, setInputValue] = useState('');
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  useEffect(() => {
    if (inputValue.length > 2) {
      setLoading(true);
      fetch(`http://localhost:5000/autocomplete/${inputValue}`)
        .then((res) => res.json())
        .then((data) => {
          setOptions(data.suggestions);
          setLoading(false);
        })
        .catch((err) => {
          console.error('Failed to fetch suggestions', err);
          setLoading(false);
        });
    }
  }, [inputValue]);

  return (
    <StyledContainer>
      <Typography variant={isMobile ? 'h4' : 'h2'} gutterBottom>
        Type to autocomplete
      </Typography>
      <Autocomplete
        options={options}
        loading={loading}
        loadingText="Fetching suggestions..."
        noOptionsText="No suggestions"
        renderInput={(params) => (
          <TextField
            {...params}
            label="Search"
            variant="outlined"
            sx={{ width: 400 }}
            onChange={(e) => setInputValue(e.target.value)}
            fullWidth
            InputProps={{
              ...params.InputProps,
              endAdornment: (
                <>
                  {loading ? (
                    <CircularProgress color="inherit" size={20} />
                  ) : null}
                  {params.InputProps.endAdornment}
                </>
              ),
            }}
          />
        )}
      />
    </StyledContainer>
  );
};

export default App;
