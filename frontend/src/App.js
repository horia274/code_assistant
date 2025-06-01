import React, { useState } from 'react';
import {
  Container,
  TextField,
  Button,
  Box,
  Typography,
  Paper,
  IconButton,
  Collapse,
  Card,
  CardContent,
  Grid,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon, ExpandMore as ExpandMoreIcon } from '@mui/icons-material';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';

function App() {
  const [codeId, setCodeId] = useState('');
  const [code, setCode] = useState('');
  const [intent, setIntent] = useState('');
  const [tests, setTests] = useState([]);
  const [showTests, setShowTests] = useState(false);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAddTest = () => {
    setTests([...tests, { id: tests.length + 1, input: '', expected_output: '' }]);
  };

  const handleRemoveTest = (index) => {
    const newTests = tests.filter((_, i) => i !== index);
    // Update IDs to maintain sequential order
    const updatedTests = newTests.map((test, idx) => ({
      ...test,
      id: idx + 1
    }));
    setTests(updatedTests);
  };

  const handleTestChange = (index, field, value) => {
    const newTests = [...tests];
    newTests[index][field] = value;
    setTests(newTests);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setResults(null); // Clear previous results
    try {
      const response = await fetch('http://localhost:5000/analyze-code', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: codeId,
          code,
          intent,
          tests: tests.length > 0 ? tests : undefined,
        }),
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Code Analyzer
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Code ID"
              value={codeId}
              onChange={(e) => setCodeId(e.target.value)}
              margin="normal"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="User Intent"
              value={intent}
              onChange={(e) => setIntent(e.target.value)}
              margin="normal"
              placeholder="e.g., run tests and detect design patterns"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Code"
              multiline
              rows={6}
              value={code}
              onChange={(e) => setCode(e.target.value)}
              margin="normal"
            />
          </Grid>
        </Grid>

        <Box sx={{ mt: 2, mb: 2 }}>
          <Button
            variant="outlined"
            startIcon={<AddIcon />}
            onClick={() => setShowTests(!showTests)}
          >
            {showTests ? 'Hide Tests' : 'Show Tests'}
          </Button>
        </Box>

        <Collapse in={showTests}>
          <Box sx={{ mt: 2 }}>
            {tests.map((test, index) => (
              <Card key={index} sx={{ mb: 2 }}>
                <CardContent>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={5}>
                      <TextField
                        fullWidth
                        label="Input"
                        value={test.input}
                        onChange={(e) => handleTestChange(index, 'input', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={5}>
                      <TextField
                        fullWidth
                        label="Expected Output"
                        value={test.expected_output}
                        onChange={(e) => handleTestChange(index, 'expected_output', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={2}>
                      <IconButton onClick={() => handleRemoveTest(index)} color="error">
                        <DeleteIcon />
                      </IconButton>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            ))}
            <Button
              variant="outlined"
              startIcon={<AddIcon />}
              onClick={handleAddTest}
              sx={{ mt: 1 }}
            >
              Add Test Case
            </Button>
          </Box>
        </Collapse>

        <Box sx={{ mt: 3 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleSubmit}
            disabled={loading}
            fullWidth
          >
            {loading ? 'Analyzing...' : 'Analyze Code'}
          </Button>
        </Box>
      </Paper>

      {results && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h5" gutterBottom>
            Analysis Results
          </Typography>
          
          {/* Score Section */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" color="primary">
              Score: {results.score}
            </Typography>
          </Box>

          {/* Feedback Section */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Feedback
            </Typography>
            <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
              {results.feedback}
            </Typography>
          </Box>

          {/* Results Section */}
          <Typography variant="h6" gutterBottom>
            Detailed Analysis
          </Typography>
          
          {Object.entries(results.results).map(([analyzer, data]) => (
            <Accordion key={analyzer} sx={{ mb: 1 }}>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography variant="subtitle1">
                  {analyzer}
                  {data.error && (
                    <Chip 
                      label="Error" 
                      color="error" 
                      size="small" 
                      sx={{ ml: 1 }}
                    />
                  )}
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                {data.error ? (
                  <Typography color="error">{data.error}</Typography>
                ) : (
                  renderAnalyzerContent(analyzer, data)
                )}
              </AccordionDetails>
            </Accordion>
          ))}
        </Paper>
      )}
    </Container>
  );
}

function renderAnalyzerContent(analyzer, data) {
  switch (analyzer) {
    case 'DesignDetector':
      return (
        <List>
          {data.design_patterns?.map((pattern, index) => (
            <ListItem key={index}>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="subtitle1">{pattern.pattern}</Typography>
                    <Chip 
                      label={`${pattern.adherence}% adherence`} 
                      color="primary" 
                      size="small"
                    />
                    <Chip 
                      label={`${pattern.confidence}% confidence`} 
                      color="secondary" 
                      size="small"
                    />
                  </Box>
                }
                secondary={pattern.reason}
              />
            </ListItem>
          ))}
        </List>
      );

    case 'TestRunner':
      return (
        <Box>
          <Box sx={{ mb: 2, display: 'flex', gap: 2 }}>
            <Chip 
              label={`${data.passed} passed`} 
              color="success" 
            />
            <Chip 
              label={`${data.failed} failed`} 
              color="error" 
            />
          </Box>
          <List>
            {data.details?.map((test) => (
              <React.Fragment key={test.id}>
                <ListItem>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="subtitle2">Test {test.id}</Typography>
                        <Chip 
                          label={test.status} 
                          color={test.status === 'passed' ? 'success' : 'error'} 
                          size="small"
                        />
                      </Box>
                    }
                    secondary={
                      <Box sx={{ mt: 1 }}>
                        <Typography variant="body2">Input: {test.input}</Typography>
                        <Typography variant="body2">Expected: {test.expected_output}</Typography>
                        <Typography variant="body2">Actual: {test.actual_output}</Typography>
                      </Box>
                    }
                  />
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        </Box>
      );

    case 'AIDetector':
      return (
        <Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <Chip 
              label={data.ai_generated_analysis.ai_generated ? 'AI Generated' : 'Human Written'} 
              color={data.ai_generated_analysis.ai_generated ? 'warning' : 'success'} 
            />
            <Chip 
              label={`${data.ai_generated_analysis.confidence}% confidence`} 
              color="secondary" 
            />
          </Box>
          <Typography variant="body1">
            {data.ai_generated_analysis.reason}
          </Typography>
        </Box>
      );

    case 'PMDRunner':
      return (
        <List>
          {data.violations?.map((violation, index) => (
            <ListItem key={index}>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="subtitle2">
                      {violation.rule}
                    </Typography>
                    <Chip 
                      label={`Priority ${violation.priority}`} 
                      color={violation.priority <= 2 ? 'error' : 'warning'} 
                      size="small"
                    />
                    <Chip 
                      label={violation.ruleset} 
                      color="info" 
                      size="small"
                    />
                  </Box>
                }
                secondary={
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      {violation.description}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                      <Typography variant="caption" color="text.secondary">
                        Line: {violation.beginline}-{violation.endline}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Column: {violation.begincolumn}-{violation.endcolumn}
                      </Typography>
                      {violation.externalInfoUrl && (
                        <Typography variant="caption">
                          <a 
                            href={violation.externalInfoUrl} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            style={{ color: 'inherit', textDecoration: 'underline' }}
                          >
                            More Info
                          </a>
                        </Typography>
                      )}
                    </Box>
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
      );

    case 'StyleChecker':
      return (
        <List>
          {data.violations?.map((violation, index) => (
            <ListItem key={index}>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="subtitle2">
                      {violation.message}
                    </Typography>
                  </Box>
                }
                secondary={
                  <Box sx={{ mt: 1 }}>
                    {violation.line && (
                      <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.5 }}>
                        Line: {violation.line}
                      </Typography>
                    )}
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
      );

    default:
      return (
        <SyntaxHighlighter language="json" style={docco}>
          {JSON.stringify(data, null, 2)}
        </SyntaxHighlighter>
      );
  }
}

export default App; 