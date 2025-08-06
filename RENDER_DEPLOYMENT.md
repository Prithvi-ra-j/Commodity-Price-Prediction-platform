# 🚀 Render Deployment Guide

This guide will help you deploy your Commodity Price Platform on Render, which supports both FastAPI backend and Streamlit frontend.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Environment Variables**: Configure as needed

## 🏗️ Deployment Steps

### Step 1: Prepare Your Repository

Your repository should have these files:
- `render.yaml` - Render configuration
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification
- `api/main.py` - FastAPI backend
- `dashboard/app.py` - Streamlit frontend

### Step 2: Deploy on Render

1. **Login to Render Dashboard**
   - Go to [dashboard.render.com](https://dashboard.render.com)
   - Sign in with your account

2. **Create New Blueprint Instance**
   - Click "New +" button
   - Select "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Configure Services**
   - Render will create two services:
     - `commodity-api` (FastAPI backend)
     - `commodity-dashboard` (Streamlit frontend)

4. **Set Environment Variables** (Optional)
   - Go to each service settings
   - Add custom environment variables if needed

### Step 3: Wait for Deployment

- **Build Time**: 5-10 minutes for initial deployment
- **Health Checks**: Services will be available once health checks pass
- **URLs**: Render will provide URLs for both services

## 🔧 Configuration Details

### FastAPI Backend (`commodity-api`)
- **URL**: `https://commodity-api.onrender.com`
- **Health Check**: `/health`
- **Port**: Automatically assigned by Render
- **Environment**: Python 3.11

### Streamlit Frontend (`commodity-dashboard`)
- **URL**: `https://commodity-dashboard.onrender.com`
- **Health Check**: `/`
- **Port**: Automatically assigned by Render
- **Environment**: Python 3.11

## 🌐 Access Your Application

Once deployed, you can access:

- **API Documentation**: `https://commodity-api.onrender.com/docs`
- **Dashboard**: `https://commodity-dashboard.onrender.com`
- **Health Check**: `https://commodity-api.onrender.com/health`

## 🔄 Auto-Deployment

Both services are configured with:
- **Auto-deploy**: Enabled (deploys on every push to main branch)
- **Health checks**: Automatic monitoring
- **Logs**: Available in Render dashboard

## 🛠️ Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `requirements.txt` for dependency conflicts
   - Ensure Python 3.11 compatibility
   - Review build logs in Render dashboard

2. **Health Check Failures**
   - Verify `/health` endpoint works locally
   - Check if database initialization is needed
   - Review service logs

3. **API Connection Issues**
   - Ensure `API_BASE_URL` environment variable is set correctly
   - Check CORS configuration in FastAPI
   - Verify network connectivity between services

### Debugging Steps

1. **Check Logs**
   - Go to service dashboard in Render
   - Click on "Logs" tab
   - Look for error messages

2. **Test Locally**
   - Run services locally to verify functionality
   - Use `python run.py` to test both services

3. **Environment Variables**
   - Verify all required environment variables are set
   - Check for typos in variable names

## 📊 Monitoring

### Render Dashboard Features
- **Real-time logs**: Monitor application logs
- **Metrics**: CPU, memory usage
- **Deployments**: Track deployment history
- **Health status**: Service availability

### Custom Monitoring
- **API Health**: `/health` endpoint
- **Dashboard Status**: Streamlit health checks
- **Database**: SQLite file persistence

## 🔒 Security Considerations

1. **Environment Variables**
   - Store sensitive data in Render environment variables
   - Never commit API keys to repository

2. **CORS Configuration**
   - FastAPI is configured to allow all origins for development
   - Consider restricting for production

3. **Database Security**
   - SQLite database is file-based
   - Consider using external database for production

## 💰 Cost Optimization

### Free Tier Limits
- **Build minutes**: 500 minutes/month
- **Runtime hours**: 750 hours/month
- **Bandwidth**: 100GB/month

### Optimization Tips
- Use `.dockerignore` to reduce build context
- Optimize dependencies in `requirements.txt`
- Consider using external database for persistence

## 🚀 Production Considerations

1. **Database**: Consider PostgreSQL for production
2. **Caching**: Add Redis for session management
3. **CDN**: Use Cloudflare for static assets
4. **Monitoring**: Add application performance monitoring
5. **Backup**: Implement database backup strategy

## 📞 Support

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Community**: [Render Community](https://community.render.com)
- **Status**: [status.render.com](https://status.render.com)

---

**Your commodity platform will be live at:**
- **API**: `https://commodity-api.onrender.com`
- **Dashboard**: `https://commodity-dashboard.onrender.com` 