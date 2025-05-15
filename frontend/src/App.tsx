import { useState } from 'react';
import { Box, Container, Typography, Paper, CircularProgress } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, LineChart, Line } from 'recharts';

interface AnalysisResponse {
  summary: {
    total: number;
  };
  by_category: Record<string, number>;
  daily_spending: Array<{
    date: string;
    amount: number;
  }>;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF6B6B'];

function App() {
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setLoading(true);
      setError(null);

      try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('http://localhost:8000/api/analyze', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Failed to analyze file');
        }

        const data = await response.json();
        setAnalysis(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
    },
    multiple: false,
  });

  const pieData = analysis
    ? Object.entries(analysis.by_category).map(([name, value]) => ({
        name,
        value,
      }))
    : [];

  const barData = analysis
    ? Object.entries(analysis.by_category).map(([name, value]) => ({
        name,
        amount: value,
      }))
    : [];

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Finance Analyzer
        </Typography>

        <Paper
          {...getRootProps()}
          sx={{
            p: 3,
            mb: 4,
            textAlign: 'center',
            cursor: 'pointer',
            bgcolor: isDragActive ? 'action.hover' : 'background.paper',
          }}
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <Typography>Drop the CSV file here...</Typography>
          ) : (
            <Typography>Drag and drop a CSV file here, or click to select one</Typography>
          )}
        </Paper>

        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        )}

        {error && (
          <Typography color="error" align="center" sx={{ my: 2 }}>
            {error}
          </Typography>
        )}

        {analysis && (
          <>
            <Typography variant="h5" gutterBottom>
              Summary Statistics
            </Typography>
            <Typography variant="body1" gutterBottom>
              Total Spending: ${analysis.summary.total.toFixed(2)}
            </Typography>

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4, my: 4 }}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Spending by Category (Pie Chart)
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                  <PieChart width={400} height={400}>
                    <Pie
                      data={pieData}
                      cx={200}
                      cy={200}
                      labelLine={false}
                      outerRadius={150}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {pieData.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </Box>
              </Paper>

              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Spending by Category (Bar Chart)
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                  <BarChart width={600} height={300} data={barData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="amount" fill="#8884d8" name="Amount" />
                  </BarChart>
                </Box>
              </Paper>

              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Daily Spending Trend
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'center' }}>
                  <LineChart width={600} height={300} data={analysis.daily_spending}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="amount" stroke="#8884d8" name="Amount" />
                  </LineChart>
                </Box>
              </Paper>
            </Box>
          </>
        )}
      </Box>
    </Container>
  );
}

export default App;
